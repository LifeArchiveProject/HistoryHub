import yaml
import os
import sys

def get_base_path():
    """获取应用程序的基础路径"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的exe运行
        base_path = sys._MEIPASS
    else:
        # 如果是直接运行python脚本
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return base_path

def get_config_path():
    """获取配置文件路径"""
    base_path = get_base_path()
    return os.path.join(base_path, 'config', 'config.yaml')

def load_config():
    config_path = get_config_path()
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"找不到配置文件: {config_path}")
        print(f"当前目录: {os.getcwd()}")
        print(f"sys._MEIPASS: {getattr(sys, '_MEIPASS', 'Not found')}")
        raise

def get_output_path(filename):
    base_path = get_base_path()
    output_dir = os.path.join(base_path, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return os.path.join(output_dir, filename)
