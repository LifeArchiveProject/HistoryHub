import asyncio
import logging
import os
import sys
import threading
from datetime import datetime
from typing import Optional, List
import traceback

import httpx
import schedule
import yaml

from scripts.scheduler_db_enhanced import EnhancedSchedulerDB  # 修改为导入增强版数据库
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
        self.tasks = {}
        self.daily_tasks = {}
        self.task_chains = {}  # 通过依赖关系构建的任务链
        self.scheduler = None
        self.task_status = {}
        self.chain_status = {}
        self.is_running = False
        self.log_capture = None
        self.current_log_file = None
        # 移除默认值，确保配置必须从配置文件中读取
        self.base_url = None
        
        # 获取增强版数据库实例
        self.db = EnhancedSchedulerDB.get_instance()
        
        # 加载配置（会设置self.base_url）
        self.load_scheduler_config()
        self._initialized = True  # 标记为已初始化

    def load_scheduler_config(self):
        """加载调度器配置"""
        try:
            base_path = get_base_path()
            config_file = os.path.join(base_path, 'config', 'scheduler_config.yaml')
            
            if not os.path.exists(config_file):
                logger.warning(f"调度器配置文件不存在: {config_file}")
                return
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 提取基础URL
            if 'base_url' in config:
                self.base_url = config['base_url']
                logger.info(f"设置基础URL: {self.base_url}")
            
            # 处理错误处理配置
            if 'error_handling' in config:
                self.notify_on_failure = config['error_handling'].get('notify_on_failure', True)
                self.stop_on_failure = config['error_handling'].get('stop_on_failure', True)
            
            # 处理调度器配置
            if 'scheduler' in config:
                scheduler_config = config['scheduler']
                self.log_level = getattr(logging, scheduler_config.get('log_level', 'INFO'))
                if 'retry' in scheduler_config:
                    self.retry_delay = scheduler_config['retry'].get('delay', 60)
                    self.max_retry_attempts = scheduler_config['retry'].get('max_attempts', 3)
            
            # 清空现有任务
            self.tasks = {}
            
            # 检查数据库是否已初始化（通过检查是否有任何主任务）
            main_tasks = self.db.get_all_main_tasks()
            
            if not main_tasks and 'tasks' in config:
                # 数据库未初始化，从配置文件加载
                logger.info("数据库未初始化，从配置文件加载任务")
                for task_id, task_config in config['tasks'].items():
                    # 创建新任务
                    task_name = task_config.get('name', task_id)
                    endpoint = task_config.get('endpoint', '')
                    method = task_config.get('method', 'GET')
                    params = task_config.get('params', {})
                    
                    # 获取调度配置
                    schedule_config = task_config.get('schedule', {})
                    schedule_type = schedule_config.get('type', 'daily')
                    schedule_time = schedule_config.get('time') if schedule_type == 'daily' else None
                    schedule_delay = schedule_config.get('delay') if schedule_type == 'once' else None
                    
                    # 判断是否为主任务或子任务
                    task_type = 'main'  # 默认为主任务
                    parent_id = None
                    sequence_number = None
                    
                    # 获取依赖项
                    requires = task_config.get('requires', [])
                    
                    # 将任务保存到数据库
                    task_data = {
                        'name': task_name,
                        'endpoint': endpoint,
                        'method': method,
                        'params': params,
                        'task_type': task_type,
                        'parent_id': parent_id,
                        'sequence_number': sequence_number,
                        'schedule_type': schedule_type,
                        'schedule_time': schedule_time,
                        'schedule_delay': schedule_delay,
                        'enabled': True
                    }
                    
                    self.db.create_main_task(task_id, task_data)
                    
                    # 添加依赖关系
                    for dep in requires:
                        self.db.add_task_dependency(task_id, dep)
            else:
                # 数据库已初始化，直接从数据库加载
                logger.info("从数据库加载任务")
                for task_data in main_tasks:
                    task_id = task_data['task_id']
                    self.tasks[task_id] = task_data
            
            # 构建任务链
            self._build_task_chains()
            
            # 设置每日任务
            self._setup_daily_tasks()
            
            logger.info(f"成功加载 {len(self.tasks)} 个任务，{len(self.daily_tasks)} 个每日任务，{len(self.task_chains)} 个任务链")
            
            self._initialized = True
        except Exception as e:
            logger.error(f"加载调度器配置失败: {str(e)}")
            traceback_str = traceback.format_exc()
            logger.debug(f"错误详情: {traceback_str}")

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
        """构建任务链（基于增强版数据库）"""
        task_chains = {}
        
        # 从数据库获取所有任务依赖关系
        for task_id in self.tasks:
            # 获取任务依赖项
            dependencies = self.db.get_task_dependencies(task_id)
            
            # 如果有依赖，就把当前任务添加到它们的后续任务中
            for dep in dependencies:
                if dep not in task_chains:
                    task_chains[dep] = []
                if task_id not in task_chains[dep]:
                    task_chains[dep].append(task_id)
        
        self.task_chains = task_chains
        logger.info(f"构建了 {len(task_chains)} 个任务链")
        
        # 输出每个任务链的详情
        for source, targets in task_chains.items():
            logger.info(f"任务链: {source} -> {', '.join(targets)}")
    
    def _setup_daily_tasks(self):
        """设置每日任务的调度"""
        now = datetime.now()
        
        # 先清除所有现有的调度任务
        schedule.clear()
        schedule.jobs.clear()
        
        # 重置所有任务的状态
        self.task_status.clear()
        
        # 创建一个同步的执行函数
        def sync_execute_task(task_name):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            try:
                task = loop.create_task(self.execute_task_chain(task_name))
                loop.run_until_complete(asyncio.gather(task))
            except Exception as e:
                print(f"执行任务时发生错误: {str(e)}")
            finally:
                if loop and not loop.is_running():
                    loop.close()
        
        for task_name, task in self.tasks.items():
            if task.get('schedule_type') == 'daily':
                # 从数据库获取任务的启用状态
                task_data = self.db.get_main_task_by_id(task_name)
                is_enabled = bool(task_data.get('enabled', False)) if task_data else False
                
                # 只调度启用的任务
                if is_enabled:
                    schedule_time = task.get('schedule_time')
                    if not schedule_time:
                        print(f"警告: 任务 {task_name} 没有设置调度时间")
                        continue
                    
                    # 计算下次执行时间
                    next_run = self._calculate_next_run_time(schedule_time)
                    if next_run:
                        next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S')
                        self.db.update_task_status(task_name, {'next_run_time': next_run_str})
                        
                        try:
                            job = schedule.every().day.at(schedule_time).do(sync_execute_task, task_name)
                            print(f"已设置任务 {task_name} 的调度时间: {schedule_time}")
                        except Exception as e:
                            print(f"设置任务调度失败: {str(e)}")

    def add_main_task(self, task_id, task_data):
        """添加主任务"""
        # 检查是否已存在同名主任务
        if self.db.is_main_task(task_id):
            logger.warning(f"主任务 {task_id} 已存在，无法添加")
            return False
        
        result = self.db.create_main_task(task_id, task_data)
        if result:
            # 更新内存中的任务集合
            task = self.db.get_main_task_by_id(task_id)
            if task:
                self.tasks[task_id] = task
                
                # 如果是每日任务，更新每日任务集合
                if task.get('schedule_type') == 'daily':
                    self._setup_daily_tasks()
                
                logger.info(f"成功添加主任务: {task_id}")
                return True
            
        return False
    
    def add_sub_task(self, parent_id, task_id, sub_task_data):
        """添加子任务"""
        if not self.db.is_main_task(parent_id):
            logger.warning(f"父任务 {parent_id} 不存在或不是主任务，无法添加子任务")
            return False
        
        # 确保子任务数据中包含task_id
        if 'task_id' not in sub_task_data:
            sub_task_data['task_id'] = task_id
        
        result = self.db.create_sub_task(parent_id, sub_task_data)
        if result:
            logger.info(f"成功为主任务 {parent_id} 添加子任务 {task_id}")
            return True
        
        return False
    
    def update_task_dependencies(self, task_id, dependencies):
        """更新任务依赖关系"""
        # 首先移除现有依赖
        self.db.remove_all_task_dependencies(task_id)
        
        # 添加新依赖
        for dep in dependencies:
            self.db.add_task_dependency(task_id, dep)
        
        # 重新构建任务链
        self._build_task_chains()
        
        logger.info(f"成功更新任务 {task_id} 的依赖关系: {dependencies}")
        return True

    async def execute_task(self, task_id: str) -> bool:
        """执行单个任务"""
        print(f"\n=== 执行任务: {task_id} ===")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 检查任务是否存在
            if task_id not in self.tasks:
                print(f"错误: 任务 {task_id} 不存在")
                return False
            
            task = self.tasks[task_id]
            print(f"开始执行任务: {task['name']}")
            
            # 创建后台任务并等待其完成
            task_result = await self.execute_task_chain(task_id)
            
            print(f"任务 {task_id} 执行完成")
            return task_result
        
        except Exception as e:
            print(f"执行任务时发生错误: {str(e)}")
            return False

    async def execute_task_chain(self, task_id: str) -> bool:
        """执行任务链，包括主任务及其子任务"""
        print(f"\n=== 执行任务链: {task_id} ===")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 检查任务是否存在
            if task_id not in self.tasks:
                print(f"错误: 任务 {task_id} 不存在")
                return False
                
            # 检查主任务是否启用
            task_data = self.db.get_main_task_by_id(task_id)
            if not task_data or not task_data.get('enabled', False):
                print(f"主任务 {task_id} 已禁用，跳过执行")
                return False
            
            # 获取任务链
            task_chain = self._build_chain_from_task(task_id)
            if not task_chain:
                print(f"错误: 无法构建任务 {task_id} 的执行链")
                return False
            
            print(f"任务链: {' -> '.join(task_chain)}")
            
            # 依次执行任务链中的每个任务
            for chain_task_id in task_chain:
                print(f"\n执行链中的任务: {chain_task_id}")
                
                # 设置当前正在执行的任务链
                self.current_chain = task_id
                
                # 如果是主任务，先执行主任务，再执行其子任务
                if self.db.is_main_task(chain_task_id):
                    # 检查主任务是否启用
                    main_task_data = self.db.get_main_task_by_id(chain_task_id)
                    if not main_task_data or not main_task_data.get('enabled', False):
                        print(f"主任务 {chain_task_id} 已禁用，跳过执行")
                        continue
                        
                    # 执行主任务
                    success = await self._execute_single_task(chain_task_id)
                    if not success:
                        print(f"主任务 {chain_task_id} 执行失败")
                        return False
                    
                    # 获取子任务列表
                    sub_tasks = self.db.get_sub_tasks(chain_task_id)
                    if sub_tasks:
                        print(f"\n开始执行主任务 {chain_task_id} 的子任务")
                        # 按sequence_number排序子任务
                        sub_tasks.sort(key=lambda x: x.get('sequence_number', 0))
                        
                        # 依次执行子任务
                        for sub_task in sub_tasks:
                            sub_task_id = sub_task['task_id']
                            # 检查子任务是否启用
                            if sub_task.get('enabled', False):
                                print(f"\n执行子任务: {sub_task_id}")
                                sub_success = await self._execute_single_task(sub_task_id, is_sub_task=True)
                                if not sub_success:
                                    print(f"子任务 {sub_task_id} 执行失败")
                                    # 记录子任务失败但继续执行其他子任务
                                    continue
                            else:
                                print(f"子任务 {sub_task_id} 已禁用，跳过执行")
                                continue
                else:
                    # 执行普通任务
                    success = await self._execute_single_task(chain_task_id)
                    if not success:
                        print(f"任务 {chain_task_id} 执行失败")
                        return False
                
            print(f"\n任务链执行完成: {task_id}")
            return True
            
        except Exception as e:
            print(f"执行任务链时发生错误: {str(e)}")
            return False
        finally:
            # 清除当前任务链标记
            self.current_chain = None

    def find_next_task(self, current_task: str) -> Optional[str]:
        """查找下一个要执行的任务"""
        for task_name, task in self.tasks.items():
            if 'requires' in task and current_task in task['requires']:
                return task_name
        return None

    def schedule_tasks(self):
        """设置任务调度"""
        print("\n=== 开始设置任务调度 ===")
        now = datetime.now()
        print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 先清除所有现有的调度任务
        schedule.clear()
        schedule.jobs.clear()  # 确保完全清除所有任务
        print("已清除所有现有调度任务")
        
        # 重置所有任务的状态
        self.task_status.clear()
        print(f"当前已配置的任务: {list(self.tasks.keys())}")
        
        # 创建一个同步的执行函数
        def sync_execute_task(task_name):
            print(f"\n=== 调度器触发任务执行 ===")
            print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"任务名称: {task_name}")
            
            # 获取或创建事件循环
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # 在事件循环中执行异步任务
            try:
                # 创建任务并等待其完成
                task = loop.create_task(self.execute_task_chain(task_name))
                loop.run_until_complete(asyncio.gather(task))
            except Exception as e:
                print(f"执行任务时发生错误: {str(e)}")
            finally:
                # 如果我们创建了新的事件循环，需要关闭它
                if loop and not loop.is_running():
                    loop.close()
        
        for task_name, task in self.tasks.items():
            print(f"\n--- 处理任务: {task_name} ---")
            
            # 打印任务详细信息
            print(f"任务配置: {task}")
            
            if task.get('schedule_type') == 'daily':
                # 获取任务的启用状态
                task_status = self.db.get_task_status(task_name)
                is_enabled = True
                if task_status and 'enabled' in task_status:
                    is_enabled = bool(task_status['enabled'])
                print(f"任务状态: {'启用' if is_enabled else '禁用'}")
                
                # 只调度启用的任务
                if is_enabled:
                    schedule_time = task.get('schedule_time')
                    if not schedule_time:
                        print(f"警告: 任务 {task_name} 没有设置调度时间")
                        continue
                        
                    print(f"调度时间: {schedule_time}")
                    
                    # 计算下次执行时间
                    next_run = self._calculate_next_run_time(schedule_time)
                    if next_run:
                        next_run_str = next_run.strftime('%Y-%m-%d %H:%M:%S')
                        self.db.update_task_status(task_name, {'next_run_time': next_run_str})
                        print(f"计算的下次执行时间: {next_run_str}")
                        time_diff = (next_run - now).total_seconds() / 60
                        print(f"距离现在: {time_diff:.1f} 分钟")
                        
                        # 使用schedule库设置任务
                        try:
                            # 确保时间格式正确
                            if ':' not in schedule_time or len(schedule_time.split(':')) != 2:
                                raise ValueError(f"时间格式不正确: {schedule_time}, 应为 HH:MM 格式")
                            
                            print(f"正在设置schedule任务...")
                            # 使用同步函数包装异步执行
                            job = schedule.every().day.at(schedule_time).do(
                                sync_execute_task, task_name
                            )
                            
                            # 验证任务是否已正确设置
                            if job in schedule.jobs:
                                print(f"任务已成功添加到调度队列")
                                print(f"任务详情: {job}")
                                if hasattr(job, 'next_run'):
                                    print(f"Schedule库计算的下次执行时间: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                            else:
                                print(f"警告: 任务可能未成功添加到调度队列")
                        except Exception as e:
                            print(f"设置任务调度失败: {str(e)}")
                    else:
                        print(f"警告: 无法计算下次执行时间")
                else:
                    print(f"任务已禁用，跳过调度")
            elif task.get('schedule_type') == 'once':
                # 检查任务是否已执行过
                task_status = self.db.get_task_status(task_name)
                if task_status and task_status.get('last_run_time'):
                    print(f"一次性任务 {task_name} 已执行过，跳过")
                    continue
                
                delay = task.get('schedule_delay', 0)
                print(f"设置一次性任务: {task_name}, {delay}秒后执行")
                
                # 使用同步函数包装异步执行
                def delayed_sync_execute(task_name, delay):
                    import time
                    print(f"等待{delay}秒后执行任务: {task_name}")
                    time.sleep(delay)
                    sync_execute_task(task_name)
                
                # 在新线程中执行延迟任务
                import threading
                thread = threading.Thread(
                    target=delayed_sync_execute,
                    args=(task_name, delay)
                )
                thread.daemon = True
                thread.start()
        
        # 打印最终的调度状态
        print("\n=== 当前调度状态 ===")
        if not schedule.jobs:
            print("没有已调度的任务")
        else:
            for job in schedule.jobs:
                print(f"- {job}")
                if hasattr(job, 'next_run') and job.next_run:
                    time_diff = (job.next_run - now).total_seconds() / 60
                    print(f"  下次执行时间: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"  距离现在: {time_diff:.1f} 分钟")
        
        print("\n=== 任务调度设置完成 ===")

    def _calculate_next_run_time(self, time_str, allow_today=True):
        """计算下次执行时间"""
        try:
            hour, minute = map(int, time_str.split(':'))
            now = datetime.now()
            today_run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            time_diff_minutes = (today_run_time - now).total_seconds() / 60
            
            if time_diff_minutes > 0:
                next_run = today_run_time
            else:
                from datetime import timedelta
                next_run = today_run_time + timedelta(days=1)
            
            return next_run
        except Exception as e:
            error_msg = f"计算下次执行时间失败: {str(e)}"
            logging.error(error_msg, exc_info=True)
            return None

    async def run_scheduler(self):
        """运行调度器"""
        print(f"\n=== 开始运行调度器 [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ===")
        
        # 重新加载配置并设置任务
        self.load_scheduler_config()
        schedule.clear()
        schedule.jobs.clear()
        self.task_status.clear()
        self.chain_status.clear()
        self.schedule_tasks()
        
        # 打印初始调度状态
        if schedule.jobs:
            print("\n当前已调度的任务:")
            for job in schedule.jobs:
                if hasattr(job, 'next_run') and job.next_run:
                    print(f"- {job}")
                    print(f"  下次执行时间: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("\n没有已调度的任务")
        
        self.is_running = True
        last_check_minute = -1
        
        while self.is_running:
            try:
                now = datetime.now()
                current_minute = now.minute
                
                # 每分钟检查一次任务状态
                if current_minute != last_check_minute:
                    last_check_minute = current_minute
                    # 运行到期的任务
                    schedule.run_pending()
                
                # 等待1秒
                await asyncio.sleep(1)
            except Exception as e:
                error_msg = f"调度器运行错误: {str(e)}"
                print(f"\n!!! 调度器错误: {error_msg}")
                logging.error(error_msg, exc_info=True)
                
                await asyncio.sleep(60)  # 出错后等待60秒再重试
                self.reload_scheduler()

    def stop_scheduler(self):
        """停止调度器"""
        self.is_running = False
        
        # 关闭数据库连接
        if hasattr(self, 'db'):
            self.db.close()

    def reload_scheduler(self):
        """重新加载调度配置"""
        print("\n=== 重新加载调度配置 ===")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 清除所有现有的调度任务
        schedule.clear()
        schedule.jobs.clear()  # 确保完全清除所有任务
        print("已清除所有现有调度任务")
        
        # 清除内部状态
        self.task_status.clear()
        self.chain_status.clear()
        
        # 重新加载配置
        self.load_scheduler_config()
        
        # 重新设置调度
        self.schedule_tasks()
        
        # 打印当前的调度状态
        print("\n当前调度状态:")
        for job in schedule.jobs:
            print(f"- {job}")
            if hasattr(job, 'next_run') and job.next_run:
                time_diff = (job.next_run - datetime.now()).total_seconds() / 60
                print(f"  下次执行时间: {job.next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"  距离现在: {time_diff:.1f} 分钟")
        
        print("\n调度配置重新加载完成")
        
    def update_task_enabled_status(self, task_id: str, enabled: bool):
        """更新任务的启用状态并重新加载调度配置"""
        if task_id not in self.tasks:
            return False
            
        # 更新数据库中的任务状态
        self.db.update_task_status(task_id, {'enabled': 1 if enabled else 0})
        
        # 重新加载调度配置
        self.reload_scheduler()
        
        return True
        
    def update_task_schedule_time(self, task_id: str, new_time: str):
        """更新任务的调度时间"""
        print(f"\n=== 更新任务调度时间 ===")
        print(f"任务ID: {task_id}")
        print(f"新的调度时间: {new_time}")
        
        try:
            # 1. 检查任务是否存在
            if task_id not in self.tasks:
                print(f"错误: 任务 {task_id} 不存在")
                return False
            
            # 2. 验证时间格式
            try:
                datetime.strptime(new_time, "%H:%M")
            except ValueError:
                print(f"错误: 无效的时间格式 {new_time}，应为 HH:MM")
                return False
            
            # 3. 更新内存中的任务配置
            print("更新内存中的任务配置...")
            self.tasks[task_id]['schedule']['time'] = new_time
            
            # 4. 保存到配置文件
            print("保存配置到文件...")
            self._save_config_to_file()
            
            # 5. 停止当前调度器
            print("停止当前调度器...")
            old_running = self.is_running
            self.is_running = False
            schedule.clear()
            schedule.jobs.clear()
            
            # 6. 重新加载配置
            print("重新加载配置...")
            self.load_scheduler_config()
            
            # 7. 重新设置所有任务的调度
            print("重新设置任务调度...")
            self.schedule_tasks()
            
            # 8. 恢复调度器状态
            print("恢复调度器状态...")
            self.is_running = old_running
            
            # 9. 检查新任务是否已正确设置
            print("\n=== 检查新的调度设置 ===")
            found = False
            now = datetime.now()
            for job in schedule.jobs:
                if task_id in str(job):
                    found = True
                    next_run = job.next_run
                    time_diff = (next_run - now).total_seconds() / 60
                    print(f"找到任务: {job}")
                    print(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"距离现在: {time_diff:.1f} 分钟")
            
            if not found:
                print(f"警告: 未找到任务 {task_id} 的新调度设置")
                return False
            
            print("\n任务调度时间更新成功")
            return True
            
        except Exception as e:
            print(f"更新任务调度时间时发生错误: {str(e)}")
            return False
        
    def _save_config_to_file(self):
        """保存当前配置到文件"""
        try:
            # 使用与加载相同的路径逻辑
            base_path = get_base_path()
            if getattr(sys, 'frozen', False):
                config_path = os.path.join(base_path, 'config', 'scheduler_config.yaml')
            else:
                config_path = os.path.join('config', 'scheduler_config.yaml')
                
            # 如果配置文件不存在，尝试其他可能的位置
            if not os.path.exists(config_path):
                alternative_paths = [
                    os.path.join(os.path.dirname(sys.executable), 'config', 'scheduler_config.yaml'),
                    os.path.join(os.getcwd(), 'config', 'scheduler_config.yaml'),
                    os.path.join(base_path, '_internal', 'config', 'scheduler_config.yaml'),
                    os.path.join(os.path.dirname(base_path), 'config', 'scheduler_config.yaml')
                ]
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        config_path = alt_path
                        break
            
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"找不到配置文件: {config_path}")
                
            # 先读取现有配置，以保留其他设置
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # 更新任务配置
            config['tasks'] = self.tasks
            
            # 写回文件
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
                
            print(f"配置已保存到: {config_path}")
            return True
        except Exception as e:
            logging.error(f"保存配置文件失败: {str(e)}")
            raise

    def sync_execute_task(self, task_name):
        """同步执行任务的包装函数"""
        print(f"\n=== 同步执行任务: {task_name} ===")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # 获取当前事件循环，如果没有则创建新的
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                should_close_loop = True
            else:
                should_close_loop = False
            
            # 在事件循环中执行任务
            try:
                # 创建任务并等待其完成
                if loop.is_running():
                    # 如果循环已经在运行，使用asyncio.run_coroutine_threadsafe
                    future = asyncio.run_coroutine_threadsafe(
                        self.execute_task_chain(task_name), 
                        loop
                    )
                    result = future.result()
                else:
                    # 如果循环未运行，正常执行
                    task = asyncio.ensure_future(self.execute_task_chain(task_name), loop=loop)
                    result = loop.run_until_complete(task)
                return result
            finally:
                # 只关闭我们创建的事件循环
                if should_close_loop and not loop.is_running():
                    loop.close()
        except Exception as e:
            print(f"执行任务时发生错误: {str(e)}")
            return False

    async def _execute_single_task(self, task_id: str, is_sub_task: bool = False) -> bool:
        """执行单个任务（主任务或子任务）"""
        print(f"\n=== 执行{'子' if is_sub_task else ''}任务: {task_id} ===")
        
        start_time = datetime.now()
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        triggered_by = "manual" if not hasattr(self, 'current_chain') else f"chain:{self.current_chain}"
        
        try:
            task = None
            if is_sub_task:
                task = self.db.get_subtask_by_id(task_id)
            else:
                task = self.tasks.get(task_id)
            
            if not task:
                print(f"错误: {'子' if is_sub_task else ''}任务 {task_id} 不存在")
                self._record_task_failure(task_id, start_time_str, "任务不存在", triggered_by)
                return False
            
            url = f"{self.base_url}{task['endpoint']}"
            method = task.get('method', 'GET').upper()
            params = task.get('params', {})
            timeout = task.get('timeout', 300)
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == 'GET':
                    response = await client.get(url, params=params)
                else:
                    response = await client.post(url, json=params)
                    
                end_time = datetime.now()
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                duration = (end_time - start_time).total_seconds()
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        print(f"任务 {task_id} 执行成功")
                        self.task_status[task_id] = True
                        self.db.record_task_execution_enhanced(
                            task_id=task_id,
                            start_time=start_time_str,
                            end_time=end_time_str,
                            duration=duration,
                            status="success",
                            triggered_by=triggered_by,
                            output=str(result)
                        )
                        return True
                    else:
                        error_msg = result.get('message', '未知错误')
                        print(f"任务 {task_id} 执行失败: {error_msg}")
                        self._record_task_failure(task_id, start_time_str, error_msg, triggered_by)
                        return False
                else:
                    error_msg = f"请求失败: {response.status_code}"
                    print(f"任务 {task_id} 请求失败: {response.status_code}")
                    self._record_task_failure(task_id, start_time_str, error_msg, triggered_by)
                    return False
                
        except Exception as e:
            error_msg = str(e)
            print(f"执行任务时发生错误: {error_msg}")
            self._record_task_failure(task_id, start_time_str, error_msg, triggered_by)
            return False

    def _record_task_failure(self, task_id, start_time_str, error_msg, triggered_by):
        """记录任务失败信息"""
        end_time = datetime.now()
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
        duration = (datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S') - 
                   datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')).total_seconds()
        
        self.task_status[task_id] = False
        self.db.record_task_execution_enhanced(
            task_id=task_id,
            start_time=start_time_str,
            end_time=end_time_str,
            duration=duration,
            status="fail",
            error_message=error_msg,
            triggered_by=triggered_by
        )

    def _build_chain_from_task(self, task_id: str) -> List[str]:
        """根据任务ID构建执行链
        
        Args:
            task_id: 任务ID
            
        Returns:
            List[str]: 任务执行顺序列表
        """
        print(f"构建任务 {task_id} 的执行链")
        
        try:
            # 如果任务不存在，返回空列表
            if task_id not in self.tasks:
                print(f"任务 {task_id} 不存在")
                return []
            
            # 获取任务的依赖项
            dependencies = self.db.get_task_dependencies(task_id)
            print(f"任务 {task_id} 的依赖项: {dependencies}")
            
            # 如果没有依赖，只返回当前任务
            if not dependencies:
                print(f"任务 {task_id} 没有依赖项，返回单任务链")
                return [task_id]
            
            # 构建完整的执行链
            execution_chain = []
            
            # 首先添加所有依赖任务
            for dep in dependencies:
                # 递归构建依赖任务的执行链
                dep_chain = self._build_chain_from_task(dep)
                # 添加未包含的任务
                for task in dep_chain:
                    if task not in execution_chain:
                        execution_chain.append(task)
            
            # 最后添加当前任务
            if task_id not in execution_chain:
                execution_chain.append(task_id)
            
            print(f"任务 {task_id} 的执行链: {' -> '.join(execution_chain)}")
            return execution_chain
            
        except Exception as e:
            print(f"构建任务链时发生错误: {str(e)}")
            return [task_id]  # 出错时至少返回当前任务

    def delete_main_task(self, task_id: str) -> bool:
        """删除主任务"""
        if task_id not in self.tasks:
            logger.warning(f"任务 {task_id} 不存在")
            return False
        
        result = self.db.delete_main_task(task_id)
        if result:
            # 从内存中删除任务
            self.tasks.pop(task_id, None)
            # 如果是每日任务，也从每日任务集合中删除
            self.daily_tasks.pop(task_id, None)
            # 重新构建任务链
            self._build_task_chains()
            logger.info(f"成功删除主任务: {task_id}")
            return True
        
        return False

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