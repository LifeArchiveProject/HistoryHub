import subprocess
import os
import shutil

def build():
    """执行打包过程"""
    try:
        # 确保 yutto.exe 存在
        yutto_exe = os.path.join('.venv', 'Scripts', 'yutto.exe')
        if not os.path.exists(yutto_exe):
            raise FileNotFoundError(f"找不到 yutto.exe: {yutto_exe}")

        print(f"找到 yutto.exe: {yutto_exe}")

        # 执行PyInstaller打包
        subprocess.run([
            'pyinstaller',
            '--clean',
            '--noconfirm',
            'app.spec'
        ], check=True)
        
        print("\n打包完成！程序位于 dist/BilibiliHistoryAnalyzer 文件夹中")

        # 复制 yutto.exe 到输出目录
        dist_dir = os.path.join('dist', 'BilibiliHistoryAnalyzer')
        if os.path.exists(yutto_exe):
            try:
                shutil.copy2(yutto_exe, dist_dir)
                print(f"已复制 yutto.exe 到 {dist_dir}")
            except Exception as e:
                print(f"复制 yutto.exe 时出错: {e}")
        else:
            print(f"警告: 找不到 {yutto_exe} 文件")

        # 验证文件是否已复制
        copied_yutto = os.path.join(dist_dir, 'yutto.exe')
        if os.path.exists(copied_yutto):
            print(f"确认 yutto.exe 已成功复制到: {copied_yutto}")
        else:
            print(f"警告: yutto.exe 未能成功复制到 {copied_yutto}")

    except subprocess.CalledProcessError as e:
        print(f"打包过程出错: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == '__main__':
    build() 