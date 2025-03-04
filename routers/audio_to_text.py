"""
音频转文字API路由
处理视频语音转文字的API接口
"""

import os
import time
import asyncio
import signal
import torch
from typing import Optional, List, Dict, Tuple
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from faster_whisper import WhisperModel
import logging
import traceback

from scripts.utils import load_config

# 设置日志格式
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建API路由
router = APIRouter()
config = load_config()

# 全局模型变量，延迟加载以节省资源
whisper_model = None
model_loading = False
model_lock = asyncio.Lock()

# 添加信号处理
def handle_interrupt(signum, frame):
    """处理中断信号"""
    global whisper_model
    print("\n正在清理资源...")
    try:
        if whisper_model is not None:
            del whisper_model
            whisper_model = None
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
        print("资源已清理")
    except Exception as e:
        print(f"清理资源时出错: {str(e)}")
    # 不再调用 os._exit(0)，让服务继续运行

# 注册信号处理器
signal.signal(signal.SIGINT, handle_interrupt)
signal.signal(signal.SIGTERM, handle_interrupt)

# 定义请求和响应模型
class TranscribeRequest(BaseModel):
    audio_path: str = Field(..., description="音频文件路径，可以是相对路径或绝对路径")
    model_size: str = Field("tiny", description="模型大小，可选值: tiny, base, small, medium, large-v1, large-v2, large-v3")
    language: str = Field("zh", description="语言代码，默认为中文")
    cid: int = Field(..., description="视频的CID，用于分类存储和命名结果")

class TranscribeResponse(BaseModel):
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="处理结果或错误信息")
    duration: Optional[float] = Field(None, description="音频时长(秒)")
    processing_time: Optional[float] = Field(None, description="处理时间(秒)")
    language_detected: Optional[str] = Field(None, description="检测到的语言")
    cid: Optional[int] = Field(None, description="处理时使用的CID")

class SystemInfo(BaseModel):
    os_name: str = Field(..., description="操作系统名称")
    os_version: str = Field(..., description="操作系统版本")
    python_version: str = Field(..., description="Python版本")
    cuda_available: bool = Field(..., description="是否支持CUDA")
    cuda_version: Optional[str] = Field(None, description="CUDA版本")
    gpu_info: Optional[List[Dict[str, str]]] = Field(None, description="GPU信息")
    cuda_setup_guide: Optional[str] = Field(None, description="CUDA安装指南")

class ModelInfo(BaseModel):
    model_size: str = Field(..., description="模型大小")
    is_downloaded: bool = Field(..., description="模型是否已下载")
    model_path: Optional[str] = Field(None, description="模型文件路径")
    download_link: Optional[str] = Field(None, description="模型下载链接")
    file_size: Optional[str] = Field(None, description="模型文件大小")

class EnvironmentCheckResponse(BaseModel):
    system_info: SystemInfo
    models_info: Dict[str, ModelInfo]
    recommended_device: str = Field(..., description="推荐使用的设备(cuda/cpu)")
    compute_type: str = Field(..., description="推荐的计算类型(float16/int8)")

class WhisperModelInfo(BaseModel):
    """Whisper模型信息"""
    name: str = Field(..., description="模型名称")
    description: str = Field(..., description="模型描述")
    is_downloaded: bool = Field(..., description="是否已下载")
    path: Optional[str] = Field(None, description="模型路径")
    params_size: str = Field(..., description="参数大小")
    recommended_use: str = Field(..., description="推荐使用场景")

async def load_model(model_size, device=None, compute_type=None):
    """加载Whisper模型"""
    global whisper_model, model_loading
    
    try:
        # 检查是否已加载相同型号的模型
        if whisper_model is not None and whisper_model.model_size == model_size:
            logger.info(f"使用已加载的模型: {model_size}")
            return whisper_model
            
        # 检查模型是否已下载
        is_downloaded, model_path = is_model_downloaded(model_size)
        if not is_downloaded:
            logger.error(f"模型 {model_size} 尚未下载")
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "MODEL_NOT_DOWNLOADED",
                    "message": f"模型 {model_size} 尚未下载，请先通过 /audio_to_text/models 接口查看可用模型，并确保选择已下载的模型",
                    "model_size": model_size
                }
            )
            
        # 如果其他进程正在加载模型，等待
        if model_loading:
            logger.info("其他进程正在加载模型，等待...")
            wait_start = time.time()
            while model_loading:
                # 添加超时检查
                if time.time() - wait_start > 300:  # 5分钟超时
                    raise HTTPException(
                        status_code=500,
                        detail="等待模型加载超时，请稍后重试"
                    )
                await asyncio.sleep(1)
            if whisper_model is not None and whisper_model.model_size == model_size:
                return whisper_model
        
        model_loading = True
        start_time = time.time()
        logger.info(f"开始加载模型: {model_size}")
        
        try:
            # 创建WhisperModel实例
            whisper_model = await loop.run_in_executor(
                None, 
                lambda: WhisperModel(model_size, device=device, compute_type=compute_type)
            )
            
            load_time = time.time() - start_time
            logger.info(f"模型加载完成，耗时 {load_time:.2f} 秒")
            
            # 存储模型大小信息
            whisper_model.model_size = model_size
            return whisper_model
            
        except Exception as e:
            logger.error(f"模型加载失败: {str(e)}")
            logger.error(f"错误堆栈: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"模型加载失败: {str(e)}"
            )
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"模型加载过程出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"模型加载过程出错: {str(e)}"
        )
    finally:
        model_loading = False
        logger.info("模型加载状态已重置")

def format_timestamp(seconds):
    """将秒转换为完整的时间戳格式 HH:MM:SS"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_int = int(seconds % 60)
    
    # 始终返回完整的 HH:MM:SS 格式
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d}"

def save_transcript(all_segments, output_path):
    """保存转录结果为简洁格式，适合节省token"""
    print(f"准备保存转录结果到: {output_path}")
    print(f"处理的片段数量: {len(all_segments)}")
    
    # 整理数据：移除多余的空格和控制字符
    with open(output_path, "w", encoding="utf-8") as f:
        # 所有片段放在一行，用空格分隔
        transcript_lines = []
        for segment in all_segments:
            # 清理文本，替换实际换行符为空格，去除多余空格
            text = segment["text"].strip().replace("\n", " ")
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            # 格式化内容并添加到列表
            transcript_lines.append(f"{start_time}>{end_time}: {text}")
        # 将所有片段用空格连接并写入一行
        f.write(" ".join(transcript_lines))
    
    print(f"转录结果已保存: {output_path}")

async def transcribe_audio(audio_path, model_size="medium", language="zh", cid=None):
    """转录音频文件"""
    try:
        logger.info(f"开始处理音频文件: {audio_path}")
        logger.info(f"参数: model_size={model_size}, language={language}, cid={cid}")
        
        start_time = time.time()
        
        # 检查文件是否存在
        if not os.path.exists(audio_path):
            logger.error(f"音频文件不存在: {audio_path}")
            raise HTTPException(
                status_code=404,
                detail=f"文件不存在: {audio_path}"
            )
        
        # 加载模型
        logger.info("准备加载模型...")
        model = await load_model(model_size)
        logger.info("模型加载完成")
        
        # 转录音频
        logger.info("开始转录音频...")
        segments, info = model.transcribe(
            audio_path,
            language=language,
            vad_filter=True
        )
        logger.info("音频转录完成")
        
        # 处理结果
        logger.info("处理转录结果...")
        all_segments = list(segments)
        logger.info(f"转录得到 {len(all_segments)} 个片段")
        
        # 如果指定了CID，保存到对应目录
        if cid:
            logger.info(f"准备保存结果到CID目录: {cid}")
            save_dir = os.path.join("output", "stt", str(cid))
            os.makedirs(save_dir, exist_ok=True)
            
            # 保存JSON格式
            json_path = os.path.join(save_dir, f"{cid}.json")
            logger.info(f"保存JSON格式到: {json_path}")
            save_transcript(all_segments, json_path)
            logger.info("转录结果保存完成")
        
        processing_time = time.time() - start_time
        logger.info(f"总处理时间: {processing_time:.2f} 秒")
        
        return {
            "success": True,
            "message": "转录完成",
            "duration": info.duration,
            "language_detected": info.language,
            "processing_time": processing_time
        }
        
    except HTTPException as he:
        # 直接传递HTTP异常
        raise he
    except Exception as e:
        logger.error(f"转录过程出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/transcribe", response_model=TranscribeResponse, summary="转录音频文件")
async def transcribe_audio_api(request: TranscribeRequest, background_tasks: BackgroundTasks):
    """转录音频文件为文本"""
    logger.info(f"收到转录请求: {request.dict()}")
    
    try:
        # 检查文件是否存在
        if not os.path.exists(request.audio_path):
            logger.error(f"文件不存在: {request.audio_path}")
            raise HTTPException(
                status_code=404,
                detail=f"文件不存在: {request.audio_path}"
            )
        
        # 异步执行转录任务
        logger.info("开始执行转录任务...")
        result = await transcribe_audio(
            audio_path=request.audio_path,
            model_size=request.model_size,
            language=request.language,
            cid=request.cid
        )
        
        logger.info("转录任务完成")
        return result
        
    except HTTPException as he:
        # 直接传递HTTP异常
        raise he
    except Exception as e:
        logger.error(f"处理请求时出错: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

def is_model_downloaded(model_name: str) -> Tuple[bool, Optional[str]]:
    """检查模型是否已下载
    
    Args:
        model_name: 模型名称
        
    Returns:
        (是否已下载, 模型路径)
    """
    # 首先检查操作系统类型，决定缓存目录的位置
    if os.name == 'nt':  # Windows
        cache_dir = os.path.join(os.environ.get('USERPROFILE', ''), '.cache', 'huggingface', 'hub')
    else:  # macOS / Linux
        cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'huggingface', 'hub')
        
    # 可能的模型提供者列表
    providers = ["guillaumekln", "Systran"]
    
    # 检查每个可能的提供者路径
    for provider in providers:
        model_id = f"{provider}/faster-whisper-{model_name}"
        model_dir = os.path.join(cache_dir, 'models--' + model_id.replace('/', '--'))
        if os.path.exists(model_dir) and os.path.exists(os.path.join(model_dir, 'snapshots')):
            return True, model_dir
            
    return False, None

@router.get("/models", response_model=List[WhisperModelInfo])
async def list_models():
    """
    列出可用的Whisper模型，并显示每个模型的下载状态和详细信息
    
    Returns:
        模型列表，包含名称、描述、下载状态等信息
    """
    # 定义模型信息
    model_infos = [
        {
            "name": "tiny.en",
            "description": "极小型(英语专用)",
            "params_size": "39M参数",
            "recommended_use": "适用于简单的英语语音识别，对资源要求最低"
        },
        {
            "name": "base.en",
            "description": "基础型(英语专用)",
            "params_size": "74M参数",
            "recommended_use": "适用于一般的英语语音识别，速度和准确度均衡"
        },
        {
            "name": "small.en",
            "description": "小型(英语专用)",
            "params_size": "244M参数",
            "recommended_use": "适用于较复杂的英语语音识别，准确度较高"
        },
        {
            "name": "medium.en",
            "description": "中型(英语专用)",
            "params_size": "769M参数",
            "recommended_use": "适用于专业的英语语音识别，准确度高"
        },
        {
            "name": "tiny",
            "description": "极小型(多语言)",
            "params_size": "39M参数",
            "recommended_use": "适用于简单的多语言语音识别，特别是资源受限场景"
        },
        {
            "name": "base",
            "description": "基础型(多语言)",
            "params_size": "74M参数",
            "recommended_use": "适用于一般的多语言语音识别，平衡性能和资源占用"
        },
        {
            "name": "small",
            "description": "小型(多语言)",
            "params_size": "244M参数",
            "recommended_use": "适用于较复杂的多语言语音识别，准确度和性能均衡"
        },
        {
            "name": "medium",
            "description": "中型(多语言)",
            "params_size": "769M参数",
            "recommended_use": "适用于专业的多语言语音识别，高准确度"
        },
        {
            "name": "large-v1",
            "description": "大型V1",
            "params_size": "1550M参数",
            "recommended_use": "适用于要求极高准确度的场景，支持所有语言"
        },
        {
            "name": "large-v2",
            "description": "大型V2",
            "params_size": "1550M参数",
            "recommended_use": "V1的改进版本，提供更好的多语言支持"
        },
        {
            "name": "large-v3",
            "description": "大型V3",
            "params_size": "1550M参数",
            "recommended_use": "最新版本，提供最佳的识别效果和语言支持"
        }
    ]
    
    result = []
    for model_info in model_infos:
        is_downloaded, model_path = is_model_downloaded(model_info["name"])
        result.append(WhisperModelInfo(
            name=model_info["name"],
            description=model_info["description"],
            is_downloaded=is_downloaded,
            path=model_path if is_downloaded else None,
            params_size=model_info["params_size"],
            recommended_use=model_info["recommended_use"]
        ))
    
    return result

@router.get("/find_audio", summary="根据CID查找音频文件路径")
async def find_audio_by_cid(cid: int):
    """
    根据CID查找对应的音频文件路径
    
    Args:
        cid: 视频的CID
        
    Returns:
        音频文件的完整路径
    """
    try:
        # 构建基础下载目录路径
        base_dir = os.path.join("./output/download_video")
        
        # 遍历所有文件夹，查找包含_cid的文件夹
        audio_path = None
        for root, dirs, files in os.walk(base_dir):
            # 检查目录名是否以_cid结尾
            if root.endswith(f"_{cid}"):
                # 在该目录下查找包含_cid的文件
                for file in files:
                    if file.endswith(f"_{cid}.m4a") or file.endswith(f"_{cid}.mp3") or file.endswith(f"_{cid}.wav"):
                        audio_path = os.path.join(root, file)
                        break
                if audio_path:
                    break
        
        if not audio_path:
            raise HTTPException(
                status_code=404,
                detail=f"未找到CID为{cid}的音频文件"
            )
        
        return {
            "cid": cid,
            "audio_path": audio_path
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"查找音频文件时出错: {str(e)}"
        )

def get_cuda_setup_guide(os_name: str) -> str:
    """根据操作系统生成CUDA安装指南"""
    if os_name.lower() == "windows":
        return """Windows CUDA安装步骤：
1. 访问 NVIDIA 驱动下载页面：https://www.nvidia.cn/Download/index.aspx
2. 下载并安装适合您显卡的最新驱动
3. 访问 NVIDIA CUDA 下载页面：https://developer.nvidia.cn/cuda-downloads
4. 选择Windows版本下载并安装CUDA Toolkit
5. 安装完成后重启系统
6. 在命令行中输入 'nvidia-smi' 验证安装"""
    elif os_name.lower() == "linux":
        return """Linux CUDA安装步骤：
1. 检查系统是否有NVIDIA显卡：
   lspci | grep -i nvidia

2. 安装NVIDIA驱动：
   Ubuntu/Debian:
   sudo apt update
   sudo apt install nvidia-driver-xxx（替换xxx为最新版本号）

   CentOS:
   sudo dnf install nvidia-driver

3. 安装CUDA Toolkit：
   访问：https://developer.nvidia.com/cuda-downloads
   选择对应的Linux发行版，按照页面提供的命令安装

4. 设置环境变量：
   echo 'export PATH=/usr/local/cuda/bin:$PATH' >> ~/.bashrc
   echo 'export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
   source ~/.bashrc

5. 验证安装：
   nvidia-smi
   nvcc --version"""
    else:
        return "暂不支持当前操作系统的CUDA安装指南"

def get_model_info(model_size: str) -> ModelInfo:
    """获取模型信息"""
    # faster-whisper模型路径
    model_path = os.path.expanduser(f"~/.cache/huggingface/hub/models--guillaumekln--faster-whisper-{model_size}")
    is_downloaded = os.path.exists(model_path)
    
    # 模型大小信息（近似值）
    model_sizes = {
        "tiny": "75MB",
        "base": "150MB",
        "small": "400MB",
        "medium": "1.5GB",
        "large-v1": "3GB",
        "large-v2": "3GB",
        "large-v3": "3GB"
    }
    
    return ModelInfo(
        model_size=model_size,
        is_downloaded=is_downloaded,
        model_path=model_path if is_downloaded else None,
        download_link=f"https://huggingface.co/guillaumekln/faster-whisper-{model_size}",
        file_size=model_sizes.get(model_size, "未知")
    )

@router.get("/check_environment", response_model=EnvironmentCheckResponse)
async def check_environment():
    """
    检查系统环境、CUDA支持情况
    
    返回：
    - 系统信息（操作系统、Python版本等）
    - CUDA支持情况
    - 推荐配置
    """
    try:
        import platform
        import sys
        
        # 获取系统信息
        os_name = platform.system()
        os_version = platform.version()
        python_version = sys.version
        
        # 检查CUDA支持
        cuda_available = torch.cuda.is_available()
        cuda_version = None
        gpu_info = None
        
        if cuda_available:
            cuda_version = torch.version.cuda
            gpu_info = []
            for i in range(torch.cuda.device_count()):
                gpu_info.append({
                    "name": torch.cuda.get_device_name(i),
                    "memory": f"{torch.cuda.get_device_properties(i).total_memory / 1024**3:.1f}GB"
                })
        
        # 生成CUDA安装指南
        cuda_setup_guide = None if cuda_available else get_cuda_setup_guide(os_name)
        
        # 获取系统信息
        system_info = SystemInfo(
            os_name=os_name,
            os_version=os_version,
            python_version=python_version,
            cuda_available=cuda_available,
            cuda_version=cuda_version,
            gpu_info=gpu_info,
            cuda_setup_guide=cuda_setup_guide
        )
        
        # 确定推荐设备和计算类型
        recommended_device = "cuda" if cuda_available else "cpu"
        compute_type = "float16" if cuda_available else "int8"
        
        return EnvironmentCheckResponse(
            system_info=system_info,
            models_info={},  # 移除模型信息，因为已经在 /models 接口中提供
            recommended_device=recommended_device,
            compute_type=compute_type
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"环境检查失败: {str(e)}"
        )

@router.post("/download_model", summary="下载指定的Whisper模型")
async def download_model(model_size: str):
    """
    下载指定的Whisper模型
    
    Args:
        model_size: 模型大小，可选值: tiny, base, small, medium, large-v1, large-v2, large-v3
    """
    try:
        # 检查模型是否已下载
        is_downloaded, model_path = is_model_downloaded(model_size)
        if is_downloaded:
            return {
                "status": "already_downloaded",
                "message": f"模型 {model_size} 已下载",
                "model_path": model_path
            }
        
        # 创建临时的WhisperModel实例来触发下载
        # 注意：这里会阻塞直到下载完成
        logger.info(f"开始下载模型: {model_size}")
        start_time = time.time()
        
        # 使用线程执行器来避免阻塞
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: WhisperModel(model_size, device="cpu", compute_type="int8")
        )
        
        download_time = time.time() - start_time
        logger.info(f"模型下载完成，耗时: {download_time:.2f} 秒")
        
        # 再次检查模型是否已下载
        is_downloaded, model_path = is_model_downloaded(model_size)
        if not is_downloaded:
            raise HTTPException(
                status_code=500,
                detail="模型下载似乎完成但未找到模型文件"
            )
            
        return {
            "status": "success",
            "message": f"模型 {model_size} 下载完成",
            "model_path": model_path,
            "download_time": f"{download_time:.2f}秒"
        }
        
    except Exception as e:
        logger.error(f"模型下载失败: {str(e)}")
        logger.error(f"错误堆栈: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"模型下载失败: {str(e)}"
        ) 