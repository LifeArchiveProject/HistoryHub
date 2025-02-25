import asyncio
import logging
import os
import sys
import threading
from datetime import datetime
from typing import Optional

import httpx
import schedule
import yaml

from scripts.scheduler_db import SchedulerDB  # 导入新的数据库模块
from scripts.utils import get_base_path, load_config

# 配置日志记录
logger = logging.getLogger(__name__)

class SchedulerManager:
    _instance = None
    _lock = threading.Lock()  # 添加线程锁
    
    @classmethod
    def get_instance(cls, app=None) -> 'SchedulerManager':
        """获取 SchedulerManager 的单例实例"""
        if not cls._instance:
            with cls._lock:  # 使用线程锁确保线程安全
                if not cls._instance:  # 双重检查
                    if app is None:
                        raise ValueError("First initialization requires app instance")
                    cls._instance = cls(app)
        return cls._instance

    def __init__(self, app):
        """初始化调度管理器"""
        # 防止重复初始化
        if hasattr(self, '_initialized'):  # 检查是否已初始化
            return
            
        self.app = app
        config = load_config()
        self.base_url = config['base_url']  # 直接使用配置文件中的base_url
        self.tasks = {}
        self.daily_tasks = {}
        self.task_chains = {}  # 通过依赖关系构建的任务链
        self.scheduler = None
        self.task_status = {}
        self.chain_status = {}
        self.is_running = False
        self.log_capture = None
        self.current_log_file = None
        
        # 初始化数据库
        self.db = SchedulerDB.get_instance()
        
        self.load_config()
        self._initialized = True  # 标记为已初始化

    def load_config(self):
        """加载调度配置"""
        try:
            # 使用 get_base_path 获取基础路径
            base_path = get_base_path()
            if getattr(sys, 'frozen', False):
                # 如果是打包后的exe运行，配置文件应该在_internal目录中
                config_path = os.path.join(base_path, 'config', 'scheduler_config.yaml')
            else:
                # 如果是直接运行python脚本
                config_path = os.path.join('config', 'scheduler_config.yaml')
            
            # 打印调试信息
            print(f"\n=== 调度器配置信息 ===")
            print(f"基础路径: {base_path}")
            print(f"配置文件路径: {config_path}")
            print(f"配置文件存在: {os.path.exists(config_path)}")
            
            # 如果配置文件不存在，尝试其他可能的位置
            if not os.path.exists(config_path):
                alternative_paths = [
                    os.path.join(os.path.dirname(sys.executable), 'config', 'scheduler_config.yaml'),
                    os.path.join(os.getcwd(), 'config', 'scheduler_config.yaml'),
                    os.path.join(base_path, '_internal', 'config', 'scheduler_config.yaml'),
                    os.path.join(os.path.dirname(base_path), 'config', 'scheduler_config.yaml')
                ]
                print("\n尝试其他可能的配置文件位置:")
                for alt_path in alternative_paths:
                    print(f"检查: {alt_path} - {'存在' if os.path.exists(alt_path) else '不存在'}")
                    if os.path.exists(alt_path):
                        config_path = alt_path
                        break
            
            # 打印目录内容
            print("\n目录内容:")
            print(f"基础目录 ({base_path}): {os.listdir(base_path)}")
            config_dir = os.path.dirname(config_path)
            if os.path.exists(config_dir):
                print(f"配置目录 ({config_dir}): {os.listdir(config_dir)}")
            print("=====================\n")
            
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"找不到配置文件: {config_path}")
                
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.base_url = config.get('base_url', self.base_url)
                self.tasks = config.get('tasks', {})
            logging.info(f"成功加载调度配置")
            logging.info(f"已配置的任务: {list(self.tasks.keys())}")
            
            # 分类任务
            self.daily_tasks = {}
            for task_id, task in self.tasks.items():
                schedule = task.get('schedule', {})
                if schedule.get('type') == 'daily':
                    self.daily_tasks[task_id] = task
            
            # 构建任务链
            self.task_chains = self._build_task_chains()
            
            # 初始化数据库中的任务状态记录
            self._init_task_status_in_db()
            
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            raise
            
    def _init_task_status_in_db(self):
        """初始化数据库中的任务状态记录"""
        for task_id, task in self.tasks.items():
            # 检查任务是否已在数据库中存在
            task_status = self.db.get_task_status(task_id)
            if not task_status:
                # 新任务，添加到数据库
                self.db.update_task_status(task_id, {
                    'name': task.get('name', task_id),
                    'enabled': 1
                })

    def _build_task_chains(self):
        """构建任务链（基于任务依赖关系）"""
        task_chains = {}
        
        # 查找不依赖其他任务的任务（作为链的起点）
        for task_id, task in self.tasks.items():
            if not task.get('requires', []):
                chain = self._build_chain_from_task(task_id)
                if chain:
                    task_chains[task_id] = chain
        
        return task_chains
    
    def _build_chain_from_task(self, start_task_id: str, visited=None):
        """从一个起始任务构建任务链"""
        if visited is None:
            visited = set()
            
        if start_task_id in visited:
            # 检测到循环依赖
            logger.warning(f"检测到循环依赖: {start_task_id}")
            return None
        
        visited.add(start_task_id)
        chain = [start_task_id]
        
        # 查找依赖这个任务的其他任务
        for task_id, task in self.tasks.items():
            requires = task.get('requires', [])
            if start_task_id in requires:
                sub_chain = self._build_chain_from_task(task_id, visited.copy())
                if sub_chain:
                    chain.extend(sub_chain)
        
        return chain

    async def execute_task(self, task_name: str) -> bool:
        """执行单个任务"""
        if task_name not in self.tasks:
            print(f"未找到任务: {task_name}")
            return False

        task = self.tasks[task_name]
        print(f"开始执行任务: {task_name}")
        
        # 记录任务开始执行
        start_time = datetime.now()
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        triggered_by = "manual" if not hasattr(self, 'current_chain') else f"chain:{self.current_chain}"
        
        # 获取当前任务状态，用于更新统计数据
        task_status = self.db.get_task_status(task_name) or {}
        total_runs = task_status.get('total_runs', 0) + 1
        success_runs = task_status.get('success_runs', 0)
        fail_runs = task_status.get('fail_runs', 0)
        
        try:
            # 检查依赖任务是否都成功完成
            for required_task in task.get('requires', []):
                if not self.task_status.get(required_task):
                    error_msg = f"依赖任务 {required_task} 未成功完成，无法执行 {task_name}"
                    print(error_msg)
                    
                    # 更新任务状态
                    fail_runs += 1
                    self.db.update_task_status(task_name, {
                        'last_run_time': start_time_str,
                        'last_status': 'fail',
                        'total_runs': total_runs,
                        'fail_runs': fail_runs,
                        'last_error': error_msg
                    })
                    
                    # 记录执行失败
                    self.db.record_task_execution(
                        task_id=task_name, 
                        start_time=start_time_str,
                        end_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        status="fail", 
                        error_message=error_msg,
                        triggered_by=triggered_by
                    )
                    return False

            url = f"{self.base_url}{task['endpoint']}"
            method = task.get('method', 'GET').upper()
            params = task.get('params', {})
            
            print(f"请求: {method} {url}")
            
            output_lines = []
            output_lines.append(f"开始执行: {start_time_str}")
            output_lines.append(f"请求: {method} {url}")
            if params:
                output_lines.append(f"参数: {params}")
            
            async with httpx.AsyncClient() as client:
                if method == 'GET':
                    response = await client.get(url, params=params)
                else:
                    response = await client.post(url, json=params)

                output_lines.append(f"状态码: {response.status_code}")
                
                # 计算任务执行时间
                end_time = datetime.now()
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                duration = (end_time - start_time).total_seconds()
                
                # 更新平均执行时间
                old_avg_duration = task_status.get('avg_duration', 0)
                if old_avg_duration == 0:
                    new_avg_duration = duration
                else:
                    # 加权平均，新的执行时间权重更高
                    new_avg_duration = (old_avg_duration * 0.7) + (duration * 0.3)
                
                if response.status_code == 200:
                    result = response.json()
                    output_lines.append(f"响应: {result}")
                    
                    if result.get("status") == "success":
                        self.task_status[task_name] = True
                        print(f"任务 {task_name} 执行成功")
                        
                        # 更新成功执行次数
                        success_runs += 1
                        
                        # 更新任务状态
                        status_update = {
                            'last_run_time': start_time_str,
                            'last_status': 'success',
                            'total_runs': total_runs,
                            'success_runs': success_runs,
                            'avg_duration': new_avg_duration
                        }
                        
                        # 对于每日任务，更新下次执行时间
                        if 'schedule' in task and task['schedule'].get('type') == 'daily':
                            time_str = task['schedule'].get('time')
                            if time_str:
                                next_run = self._calculate_next_run_time(time_str)
                                if next_run:
                                    status_update['next_run_time'] = next_run.strftime('%Y-%m-%d %H:%M:%S')
                        
                        # 更新任务状态
                        self.db.update_task_status(task_name, status_update)
                        
                        # 记录执行成功
                        self.db.record_task_execution(
                            task_id=task_name,
                            start_time=start_time_str,
                            end_time=end_time_str,
                            duration=duration,
                            status="success",
                            triggered_by=triggered_by,
                            output="\n".join(output_lines)
                        )
                        return True
                    else:
                        error_msg = result.get('message', '未知错误')
                        self.task_status[task_name] = False
                        print(f"任务 {task_name} 执行失败: {error_msg}")
                        
                        # 更新失败执行次数
                        fail_runs += 1
                        
                        # 更新任务状态
                        self.db.update_task_status(task_name, {
                            'last_run_time': start_time_str,
                            'last_status': 'fail',
                            'total_runs': total_runs,
                            'fail_runs': fail_runs,
                            'avg_duration': new_avg_duration,
                            'last_error': error_msg
                        })
                        
                        # 记录执行失败
                        self.db.record_task_execution(
                            task_id=task_name,
                            start_time=start_time_str,
                            end_time=end_time_str,
                            duration=duration,
                            status="fail",
                            error_message=error_msg,
                            triggered_by=triggered_by,
                            output="\n".join(output_lines)
                        )
                        return False
                else:
                    error_msg = f"请求失败: {response.status_code} - {response.text}"
                    self.task_status[task_name] = False
                    print(f"任务 {task_name} 请求失败: {response.status_code}")
                    
                    # 更新失败执行次数
                    fail_runs += 1
                    
                    # 更新任务状态
                    self.db.update_task_status(task_name, {
                        'last_run_time': start_time_str,
                        'last_status': 'fail',
                        'total_runs': total_runs,
                        'fail_runs': fail_runs,
                        'avg_duration': new_avg_duration,
                        'last_error': error_msg
                    })
                    
                    # 记录执行失败
                    self.db.record_task_execution(
                        task_id=task_name,
                        start_time=start_time_str,
                        end_time=end_time_str,
                        duration=duration,
                        status="fail",
                        error_message=error_msg,
                        triggered_by=triggered_by,
                        output="\n".join(output_lines)
                    )
                    return False

        except Exception as e:
            error_msg = f"执行任务时发生错误: {str(e)}"
            print(error_msg)
            self.task_status[task_name] = False
            
            # 更新失败执行次数
            fail_runs += 1
            
            # 计算任务执行时间
            end_time = datetime.now()
            end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
            duration = (end_time - start_time).total_seconds()
            
            # 更新任务状态
            self.db.update_task_status(task_name, {
                'last_run_time': start_time_str,
                'last_status': 'fail',
                'total_runs': total_runs,
                'fail_runs': fail_runs,
                'last_error': error_msg
            })
            
            # 记录执行错误
            self.db.record_task_execution(
                task_id=task_name,
                start_time=start_time_str,
                end_time=end_time_str,
                duration=duration,
                status="fail",
                error_message=error_msg,
                triggered_by=triggered_by
            )
            return False

    async def execute_task_chain(self, start_task: str):
        """执行任务链"""
        # 生成今天的任务链唯一标识
        chain_id = f"{start_task}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        chain_start_time = datetime.now()
        chain_start_time_str = chain_start_time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 检查任务链是否已执行
        if chain_id in self.chain_status:
            return
            
        # 标记任务链开始执行
        self.chain_status[chain_id] = True
        self.current_chain = chain_id
        
        # 获取任务链
        tasks_in_chain = []
        if start_task in self.task_chains:
            tasks_in_chain = self.task_chains[start_task]
        else:
            # 如果没有预定义的任务链，使用单任务作为任务链
            tasks_in_chain = [start_task]
            
        print(f"开始执行任务链 {chain_id}, 任务列表: {tasks_in_chain}")
        
        # 记录任务链的执行开始
        self.db.record_chain_execution_start(
            chain_id=chain_id,
            start_task_id=start_task,
            start_time=chain_start_time_str
        )
        
        # 执行任务链中的所有任务
        tasks_executed = []
        tasks_succeeded = []
        tasks_failed = []
        
        try:
            for task_id in tasks_in_chain:
                tasks_executed.append(task_id)
                success = await self.execute_task(task_id)
                
                if success:
                    tasks_succeeded.append(task_id)
                else:
                    tasks_failed.append(task_id)
                    # 如果任务失败，记录日志但继续执行其他任务
                    logging.warning(f"任务链 {chain_id} 中的任务 {task_id} 执行失败")
                
            # 确定任务链的整体状态
            chain_status = "success"
            if len(tasks_failed) > 0:
                chain_status = "partial_success" if len(tasks_succeeded) > 0 else "failed"
                
            # 记录任务链执行完成
            chain_end_time = datetime.now()
            chain_end_time_str = chain_end_time.strftime('%Y-%m-%d %H:%M:%S')
            chain_duration = (chain_end_time - chain_start_time).total_seconds()
            
            self.db.record_chain_execution_end(
                chain_id=chain_id,
                end_time=chain_end_time_str,
                status=chain_status,
                tasks_executed=len(tasks_executed),
                tasks_succeeded=len(tasks_succeeded),
                tasks_failed=len(tasks_failed)
            )
            
            print(f"任务链 {chain_id} 执行完成, 状态: {chain_status}, "
                  f"执行: {len(tasks_executed)}, 成功: {len(tasks_succeeded)}, 失败: {len(tasks_failed)}")
            
            return {
                "status": chain_status,
                "message": f"任务链执行完成",
                "chain_id": chain_id,
                "start_time": chain_start_time_str,
                "end_time": chain_end_time_str,
                "duration": chain_duration,
                "tasks_executed": tasks_executed,
                "tasks_succeeded": tasks_succeeded,
                "tasks_failed": tasks_failed
            }
            
        except Exception as e:
            error_message = f"执行任务链时发生错误: {str(e)}"
            logging.error(error_message)
            
            # 记录任务链执行失败
            chain_end_time = datetime.now()
            chain_end_time_str = chain_end_time.strftime('%Y-%m-%d %H:%M:%S')
            
            self.db.record_chain_execution_end(
                chain_id=chain_id,
                end_time=chain_end_time_str,
                status="error",
                tasks_executed=len(tasks_executed),
                tasks_succeeded=len(tasks_succeeded),
                tasks_failed=len(tasks_failed)
            )
            
            return {
                "status": "error",
                "message": error_message,
                "chain_id": chain_id
            }
            
        finally:
            # 任务链执行完成后，清理状态
            self.task_status.clear()
            if hasattr(self, 'current_chain'):
                delattr(self, 'current_chain')

    def find_next_task(self, current_task: str) -> Optional[str]:
        """查找下一个要执行的任务"""
        for task_name, task in self.tasks.items():
            if 'requires' in task and current_task in task['requires']:
                return task_name
        return None

    def schedule_tasks(self):
        """设置任务调度"""
        print("开始设置任务调度...")
        print(f"当前已配置的任务: {list(self.tasks.keys())}")
        
        for task_name, task in self.tasks.items():
            if 'schedule' in task:
                schedule_info = task['schedule']
                schedule_type = schedule_info['type']
                
                if schedule_type == 'daily':
                    # 获取任务的启用状态
                    task_status = self.db.get_task_status(task_name)
                    is_enabled = True
                    if task_status and 'enabled' in task_status:
                        is_enabled = bool(task_status['enabled'])
                    
                    # 只调度启用的任务
                    if is_enabled:
                        time_str = schedule_info['time']
                        # 计算下次执行时间
                        next_run = self._calculate_next_run_time(time_str)
                        if next_run:
                            self.db.set_task_next_run(task_name, next_run)
                            
                        job = schedule.every().day.at(schedule_info['time']).do(
                            lambda t=task_name: asyncio.create_task(self.execute_task_chain(t))
                        )
                        print(f"已设置每日任务: {task_name}, 时间: {schedule_info['time']}, 启用状态: {'启用' if is_enabled else '禁用'}")
                
                elif schedule_type == 'once':
                    # 检查任务是否已执行过
                    task_status = self.db.get_task_status(task_name)
                    if task_status and task_status.get('last_run_time'):
                        print(f"一次性任务 {task_name} 已执行过，跳过")
                        continue
                    
                    delay = schedule_info.get('delay', 0)
                    print(f"设置一次性任务: {task_name}, {delay}秒后执行")
                    
                    async def delayed_start(task_name):
                        print(f"等待{delay}秒后执行任务: {task_name}")
                        await asyncio.sleep(delay)
                        print(f"开始执行任务: {task_name}")
                        await self.execute_task_chain(task_name)
                    
                    # 创建异步任务
                    asyncio.create_task(delayed_start(task_name))
    
    def _calculate_next_run_time(self, time_str):
        """计算下次执行时间"""
        try:
            # 解析时间字符串，格式为 HH:MM
            hour, minute = map(int, time_str.split(':'))
            
            # 获取当前时间
            now = datetime.now()
            
            # 创建今天的执行时间
            today_run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # 如果今天的执行时间已经过了，则使用明天的时间
            if today_run_time <= now:
                # 添加一天
                from datetime import timedelta
                next_run = today_run_time + timedelta(days=1)
            else:
                next_run = today_run_time
                
            return next_run
        except Exception as e:
            logging.error(f"计算下次执行时间失败: {str(e)}")
            return None

    async def run_scheduler(self):
        """运行调度器"""
        self.is_running = True
        self.schedule_tasks()
        
        while self.is_running:
            try:
                schedule.run_pending()
                await asyncio.sleep(1)
            except Exception as e:
                logging.error(f"调度器运行错误: {e}")
                await asyncio.sleep(60)

    def stop_scheduler(self):
        """停止调度器"""
        self.is_running = False
        
        # 关闭数据库连接
        if hasattr(self, 'db'):
            self.db.close()

async def send_error_notification(error_message):
    """发送错误通知邮件"""
    config = load_config()
    email_config = config.get('email', {})
    
    subject = "Bilibili历史记录分析任务执行出错"
    body = f"""
    执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    错误信息: {error_message}
    """
    
    try:
        await send_email(
            email_config.get('smtp_server'),
            email_config.get('smtp_port'),
            email_config.get('sender'),
            email_config.get('password'),
            email_config.get('receiver'),
            subject,
            body
        )
    except Exception as e:
        print(f"发送错误通知邮件失败: {e}")
        logging.error(f"发送错误通知邮件失败: {e}", exc_info=True)