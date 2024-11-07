import os
import subprocess
import sys
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from scripts.utils import load_config

router = APIRouter()
config = load_config()

class DownloadRequest(BaseModel):
    url: str
    sessdata: Optional[str] = Field(None, description="用户的 SESSDATA")

@router.post("/download_video", summary="下载B站视频")
async def download_video(request: DownloadRequest):
    """
    下载B站视频
    
    Args:
        request: 包含视频URL和可选SESSDATA的请求对象
    """
    try:
        # 获取 yutto 可执行文件路径
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe运行
            base_path = os.path.dirname(sys.executable)
            paths_to_try = [
                os.path.join(base_path, 'yutto.exe'),  # 尝试主目录
                os.path.join(base_path, '_internal', 'yutto.exe'),  # 尝试 _internal 目录
                os.path.join(os.getcwd(), 'yutto.exe'),  # 尝试当前工作目录
                os.path.join(os.getcwd(), '_internal', 'yutto.exe')  # 尝试当前工作目录的 _internal
            ]
            
            yutto_path = None
            for path in paths_to_try:
                print(f"尝试路径: {path}")
                if os.path.exists(path):
                    yutto_path = path
                    print(f"找到 yutto.exe: {path}")
                    break
            
            if yutto_path is None:
                raise FileNotFoundError(f"找不到 yutto.exe，已尝试的路径: {', '.join(paths_to_try)}")
        else:
            # 如果是直接运行python脚本
            yutto_path = 'yutto'
            print(f"使用命令: {yutto_path}")

        if not os.path.exists(yutto_path) and getattr(sys, 'frozen', False):
            raise FileNotFoundError(f"找不到 yutto.exe，已尝试的路径: {yutto_path}")

        # 构建命令
        command = [
            yutto_path,
            request.url,
            '--dir', config['yutto']['basic']['dir'],
            '--tmp-dir', config['yutto']['basic']['tmp_dir']
        ]
        
        # 添加其他 yutto 配置
        if not config['yutto']['resource']['require_subtitle']:
            command.append('--no-subtitle')
            
        if config['yutto']['danmaku']['font_size']:
            command.extend(['--danmaku-font-size', str(config['yutto']['danmaku']['font_size'])])
            
        if config['yutto']['batch']['with_section']:
            command.append('--with-section')
            
        # 如果提供了SESSDATA，添加到命令中
        if request.sessdata:
            command.extend(['--sessdata', request.sessdata])
        elif config.get('SESSDATA'):  # 使用配置文件中的 SESSDATA
            command.extend(['--sessdata', config['SESSDATA']])

        # 设置环境变量
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'

        # 执行命令
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace',
            universal_newlines=True,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

        # 获取输出
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return {
                "status": "success",
                "message": "视频下载成功",
                "output": stdout
            }
        else:
            error_msg = stderr if stderr else stdout
            raise HTTPException(
                status_code=500,
                detail=f"下载失败: {error_msg}"
            )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="找不到 yutto 命令，请确保已正确安装"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"下载过程出错: {str(e)}"
        ) 