import subprocess

def build():
    """执行打包过程"""
    try:
        # 执行PyInstaller打包
        subprocess.run([
            'pyinstaller', '--clean', '--noconfirm', 'app.spec',
            '--add-data', '.venv/Lib/site-packages/pyecharts/datasets;./pyecharts/datasets',
            '--add-data', '.venv/Lib/site-packages/pyecharts/render/templates;./pyecharts/render/templates'
        ], check=True)
        
        print("\n打包完成！程序位于 dist/BilibiliHistoryAnalyzer 文件夹中")
    except subprocess.CalledProcessError as e:
        print(f"打包过程出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    build() 