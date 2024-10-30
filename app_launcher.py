import os
import sys
import uvicorn
from multiprocessing import freeze_support

def main():
    try:
        # 添加项目根目录到 Python 路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe运行
            base_path = os.path.dirname(sys.executable)
        else:
            # 如果是直接运行python脚本
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        sys.path.insert(0, base_path)
        
        # 启用多进程支持
        freeze_support()
        
        # 启动FastAPI应用
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=False
        )
    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        print("\n完整错误信息:")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")

if __name__ == '__main__':
    main() 