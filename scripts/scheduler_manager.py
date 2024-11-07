import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Optional, Dict, ClassVar
import threading

import httpx
import schedule
import yaml

from scripts.utils import get_base_path


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
        self.base_url = "http://localhost:8000"
        self.tasks = {}
        self.task_status = {}
        self.chain_status = {}
        self.is_running = False
        self.log_capture = None
        self.current_log_file = None
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
        except Exception as e:
            logging.error(f"加载配置文件失败: {e}")
            raise

    async def execute_task(self, task_name: str) -> bool:
        """执行单个任务"""
        if task_name not in self.tasks:
            print(f"未找到任务: {task_name}")
            return False

        task = self.tasks[task_name]
        print(f"开始执行任务: {task_name}")
        
        try:
            # 检查依赖任务是否都成功完成
            for required_task in task.get('requires', []):
                if not self.task_status.get(required_task):
                    print(f"依赖任务 {required_task} 未成功完成，无法执行 {task_name}")
                    return False

            url = f"{self.base_url}{task['endpoint']}"
            method = task.get('method', 'GET').upper()
            params = task.get('params', {})
            
            print(f"请求: {method} {url}")
            
            async with httpx.AsyncClient() as client:
                if method == 'GET':
                    response = await client.get(url, params=params)
                else:
                    response = await client.post(url, json=params)

                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "success":
                        self.task_status[task_name] = True
                        print(f"任务 {task_name} 执行成功")
                        return True
                    else:
                        self.task_status[task_name] = False
                        print(f"任务 {task_name} 执行失败: {result.get('message')}")
                        return False
                else:
                    self.task_status[task_name] = False
                    print(f"任务 {task_name} 请求失败: {response.status_code}")
                    return False

        except Exception as e:
            print(f"执行任务 {task_name} 时发生错误: {str(e)}")
            self.task_status[task_name] = False
            return False

    async def execute_task_chain(self, start_task: str):
        """执行任务链"""
        # 生成今天的任务链唯一标识
        chain_id = f"{start_task}_{datetime.now().strftime('%Y%m%d')}"
        
        # 检查任务链是否已执行
        if chain_id in self.chain_status:
            return
            
        # 标记任务链开始执行
        self.chain_status[chain_id] = True
        
        try:
            current_task = start_task
            while current_task:
                success = await self.execute_task(current_task)
                if not success:
                    break
                    
                # 查找下一个任务
                next_task = self.find_next_task(current_task)
                current_task = next_task
        except Exception as e:
            logging.error(f"任务链执行错误: {str(e)}")
        finally:
            # 任务链执行完成后，清理状态
            self.task_status.clear()

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
                    schedule.every().day.at(schedule_info['time']).do(
                        lambda t=task_name: asyncio.create_task(self.execute_task_chain(t))
                    )
                    print(f"已设置每日任务: {task_name}")
                
                elif schedule_type == 'once':
                    delay = schedule_info.get('delay', 0)
                    print(f"设置一次性任务: {task_name}, {delay}秒后执行")
                    
                    async def delayed_start(task_name):
                        print(f"等待{delay}秒后执行任务: {task_name}")
                        await asyncio.sleep(delay)
                        print(f"开始执行任务: {task_name}")
                        await self.execute_task_chain(task_name)
                    
                    # 创建异步任务
                    asyncio.create_task(delayed_start(task_name))

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