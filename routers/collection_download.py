import os
import re
from typing import Optional, List, Dict, Any, Tuple

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import httpx

from scripts.utils import load_config
from scripts.yutto_runner import run_yutto

router = APIRouter()
config = load_config()

class CollectionInfo(BaseModel):
    """合集信息"""
    is_collection: bool = Field(..., description="是否为合集")
    collection_id: Optional[str] = Field(None, description="合集ID")
    collection_title: Optional[str] = Field(None, description="合集标题")
    total_videos: Optional[int] = Field(None, description="合集中视频总数")
    current_video_index: Optional[int] = Field(None, description="当前视频在合集中的位置")
    videos: Optional[List[Dict[str, Any]]] = Field(None, description="合集中的视频列表")
    uploader_mid: Optional[int] = Field(None, description="UP主的UID")

class CollectionDownloadRequest(BaseModel):
    """合集下载请求 - 简化版，只用于整个合集下载"""
    url: str = Field(..., description="合集URL")
    cid: int = Field(..., description="视频的 CID，用于分类存储")

    # 基础下载参数
    sessdata: Optional[str] = Field(None, description="用户的 SESSDATA")
    download_cover: Optional[bool] = Field(True, description="是否下载视频封面")
    only_audio: Optional[bool] = Field(False, description="是否仅下载音频")
    video_quality: Optional[int] = Field(None, description="视频清晰度等级")
    audio_quality: Optional[int] = Field(None, description="音频码率等级")
    vcodec: Optional[str] = Field(None, description="视频编码")
    acodec: Optional[str] = Field(None, description="音频编码")
    download_vcodec_priority: Optional[str] = Field(None, description="视频下载编码优先级")
    output_format: Optional[str] = Field(None, description="输出格式")
    output_format_audio_only: Optional[str] = Field(None, description="仅包含音频流时的输出格式")
    video_only: Optional[bool] = Field(False, description="是否仅下载视频流")
    danmaku_only: Optional[bool] = Field(False, description="是否仅生成弹幕文件")
    no_danmaku: Optional[bool] = Field(False, description="是否不生成弹幕文件")
    subtitle_only: Optional[bool] = Field(False, description="是否仅生成字幕文件")
    no_subtitle: Optional[bool] = Field(False, description="是否不生成字幕文件")
    metadata_only: Optional[bool] = Field(False, description="是否仅生成媒体元数据文件")
    save_cover: Optional[bool] = Field(False, description="生成视频流封面时是否单独保存封面")
    cover_only: Optional[bool] = Field(False, description="是否仅生成视频封面")
    no_chapter_info: Optional[bool] = Field(False, description="是否不生成章节信息")

def extract_video_info_from_url(url: str) -> Dict[str, Any]:
    """
    从URL中提取视频信息
    
    Args:
        url: 视频URL
        
    Returns:
        包含视频信息的字典
    """
    # 提取BV号或AV号
    bv_match = re.search(r'BV[a-zA-Z0-9]+', url)
    av_match = re.search(r'av(\d+)', url)
    
    video_id = None
    if bv_match:
        video_id = bv_match.group()
    elif av_match:
        video_id = f"av{av_match.group(1)}"
    
    # 提取分P信息
    p_match = re.search(r'[?&]p=(\d+)', url)
    page = int(p_match.group(1)) if p_match else 1
    
    return {
        "video_id": video_id,
        "page": page,
        "original_url": url
    }

async def get_video_collection_info(url: str, sessdata: Optional[str] = None) -> CollectionInfo:
    """
    获取视频的合集信息

    Args:
        url: 视频URL
        sessdata: 可选的SESSDATA用于认证

    Returns:
        合集信息对象
    """
    try:
        video_info = extract_video_info_from_url(url)
        if not video_info["video_id"]:
            return CollectionInfo(is_collection=False)

        # 构建API请求
        api_url = f"https://api.bilibili.com/x/web-interface/view"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }

        if sessdata:
            headers['Cookie'] = f'SESSDATA={sessdata}'
        elif config.get('SESSDATA'):
            headers['Cookie'] = f'SESSDATA={config["SESSDATA"]}'

        params = {}
        if video_info["video_id"].startswith('BV'):
            params['bvid'] = video_info["video_id"]
        else:
            params['aid'] = video_info["video_id"][2:]  # 去掉'av'前缀

        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()

        if data.get('code') != 0:
            return CollectionInfo(is_collection=False)

        video_data = data.get('data', {})

        # 检查是否有合集信息
        ugc_season = video_data.get('ugc_season')
        if ugc_season:
            # 这是一个合集
            collection_info = CollectionInfo(
                is_collection=True,
                collection_id=str(ugc_season.get('id')),
                collection_title=ugc_season.get('title'),
                total_videos=len(ugc_season.get('sections', [{}])[0].get('episodes', [])),
                videos=[],
                # 添加UP主信息用于构建合集URL
                uploader_mid=video_data.get('owner', {}).get('mid')
            )

            # 获取合集中的视频列表
            episodes = ugc_season.get('sections', [{}])[0].get('episodes', [])
            for i, episode in enumerate(episodes):
                video_item = {
                    "index": i + 1,
                    "title": episode.get('title'),
                    "bvid": episode.get('bvid'),
                    "cid": episode.get('cid'),
                    "duration": episode.get('arc', {}).get('duration'),
                    "page": episode.get('page', 1)
                }
                collection_info.videos.append(video_item)

                # 检查当前视频在合集中的位置
                if episode.get('bvid') == video_info["video_id"]:
                    collection_info.current_video_index = i + 1

            return collection_info

        # 检查是否有分P视频（多P视频也可以视为一种合集）
        pages = video_data.get('pages', [])
        if len(pages) > 1:
            collection_info = CollectionInfo(
                is_collection=True,
                collection_id=video_info["video_id"],
                collection_title=video_data.get('title'),
                total_videos=len(pages),
                current_video_index=video_info["page"],
                videos=[],
                uploader_mid=video_data.get('owner', {}).get('mid')
            )

            for page in pages:
                video_item = {
                    "index": page.get('page'),
                    "title": page.get('part'),
                    "bvid": video_info["video_id"],
                    "cid": page.get('cid'),
                    "duration": page.get('duration'),
                    "page": page.get('page')
                }
                collection_info.videos.append(video_item)

            return collection_info

        # 不是合集，只是单个视频
        return CollectionInfo(is_collection=False)

    except Exception as e:
        print(f"获取合集信息时出错：{str(e)}")
        return CollectionInfo(is_collection=False)

def check_download_directories() -> Tuple[str, str]:
    """
    检查下载目录和临时目录是否存在且有写入权限

    Returns:
        下载目录和临时目录的路径元组

    Raises:
        HTTPException: 如果目录不存在或没有写入权限
    """
    download_dir = os.path.normpath(config['yutto']['basic']['dir'])
    tmp_dir = os.path.normpath(config['yutto']['basic']['tmp_dir'])

    # 创建目录（如果不存在）
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(tmp_dir, exist_ok=True)

    # 检查目录权限
    if not os.access(download_dir, os.W_OK):
        raise HTTPException(
            status_code=500,
            detail=f"没有下载目录的写入权限：{download_dir}"
        )
    if not os.access(tmp_dir, os.W_OK):
        raise HTTPException(
            status_code=500,
            detail=f"没有临时目录的写入权限：{tmp_dir}"
        )

    return download_dir, tmp_dir

def add_download_params_to_command(command: List[str], params: CollectionDownloadRequest) -> List[str]:
    """
    将下载参数添加到命令中

    Args:
        command: 命令列表
        params: 包含下载参数的对象

    Returns:
        添加了下载参数的命令列表
    """
    # 基础参数
    if params.video_quality is not None:
        command.extend(['--video-quality', str(params.video_quality)])

    if params.audio_quality is not None:
        command.extend(['--audio-quality', str(params.audio_quality)])

    if params.vcodec:
        command.extend(['--vcodec', params.vcodec])

    if params.acodec:
        command.extend(['--acodec', params.acodec])

    if params.download_vcodec_priority:
        command.extend(['--download-vcodec-priority', params.download_vcodec_priority])

    if params.output_format:
        command.extend(['--output-format', params.output_format])

    if params.output_format_audio_only:
        command.extend(['--output-format-audio-only', params.output_format_audio_only])

    # 资源选择参数
    if params.video_only:
        command.append('--video-only')

    if params.only_audio:
        command.append('--audio-only')

    if params.no_danmaku:
        command.append('--no-danmaku')

    if params.danmaku_only:
        command.append('--danmaku-only')

    if params.no_subtitle or not config['yutto']['resource']['require_subtitle']:
        command.append('--no-subtitle')

    if params.subtitle_only:
        command.append('--subtitle-only')

    if params.metadata_only:
        command.append('--metadata-only')

    if not params.download_cover:
        command.append('--no-cover')

    if params.save_cover:
        command.append('--save-cover')

    if params.cover_only:
        command.append('--cover-only')

    if params.no_chapter_info:
        command.append('--no-chapter-info')

    # 添加其他 yutto 配置
    if config['yutto']['danmaku']['font_size']:
        command.extend(['--danmaku-font-size', str(config['yutto']['danmaku']['font_size'])])

    if config['yutto']['batch']['with_section']:
        command.append('--with-section')

    # 如果提供了 SESSDATA，添加到命令中
    if params.sessdata:
        command.extend(['--sessdata', params.sessdata])
    elif config.get('SESSDATA'):
        command.extend(['--sessdata', config['SESSDATA']])

    return command

@router.get("/check_collection", summary="检查视频是否为合集")
async def check_collection(url: str, sessdata: Optional[str] = None):
    """
    检查给定的视频URL是否为合集

    Args:
        url: 视频URL
        sessdata: 可选的SESSDATA用于认证

    Returns:
        合集信息
    """
    try:
        collection_info = await get_video_collection_info(url, sessdata)
        return {
            "status": "success",
            "data": collection_info.model_dump()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"检查合集信息时出错：{str(e)}"
        )

@router.post("/download_collection", summary="下载整个合集")
async def download_collection(request: CollectionDownloadRequest):
    """
    下载B站整个合集或多P视频的所有分P

    Args:
        request: 包含合集下载参数的请求对象
    """
    try:
        # 检查下载目录和临时目录
        download_dir, tmp_dir = check_download_directories()

        # 首先检查是否为合集
        collection_info = await get_video_collection_info(request.url, request.sessdata)

        if not collection_info.is_collection:
            raise HTTPException(
                status_code=400,
                detail="提供的URL不是合集或多P视频"
            )

        # 构建下载整个合集的命令
        # 使用安全的文件名（移除特殊字符）
        safe_collection_title = "".join(c for c in collection_info.collection_title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        if collection_info.collection_id and collection_info.collection_id != collection_info.videos[0]["bvid"]:
            # 真正的合集，构建合集的专用URL
            if collection_info.uploader_mid:
                # 使用合集的专用URL格式
                collection_url = f"https://space.bilibili.com/{collection_info.uploader_mid}/channel/collectiondetail?sid={collection_info.collection_id}"
                command = [
                    collection_url,
                    '--batch',  # 批量下载模式
                    '--dir', download_dir,
                    '--tmp-dir', tmp_dir,
                    '--subpath-template', f'{safe_collection_title}_collection/{{title}}_{{username}}_{{download_date@%Y%m%d_%H%M%S}}/{{title}}',
                    '--with-metadata'
                ]
            else:
                # 如果没有UP主信息，回退到使用单个视频URL + batch模式
                video_info = extract_video_info_from_url(request.url)
                base_url = f"https://www.bilibili.com/video/{video_info['video_id']}"
                command = [
                    base_url,
                    '--batch',  # 批量下载模式
                    '--dir', download_dir,
                    '--tmp-dir', tmp_dir,
                    '--subpath-template', f'{safe_collection_title}_collection/{{title}}_{{username}}_{{download_date@%Y%m%d_%H%M%S}}/{{title}}',
                    '--with-metadata'
                ]
        else:
            # 多P视频，下载所有分P
            video_info = extract_video_info_from_url(request.url)
            base_url = f"https://www.bilibili.com/video/{video_info['video_id']}"
            command = [
                base_url,
                '--batch',  # 批量下载模式
                '--dir', download_dir,
                '--tmp-dir', tmp_dir,
                '--subpath-template', f'{safe_collection_title}_multipart/{{title}}_{{username}}_{{download_date@%Y%m%d_%H%M%S}}/{{title}}',
                '--with-metadata'
            ]

        # 添加下载参数
        command = add_download_params_to_command(command, request)

        print(f"执行合集下载命令：yutto {' '.join(command)}")
        print(f"合集信息：{collection_info.collection_title}，共 {collection_info.total_videos} 个视频")
        print("注意：如果合集中包含分P视频，yutto可能会报错，这是yutto限制，和本项目无关")

        async def event_stream():
            # 发送开始信息
            yield f"event: info\ndata: 开始下载合集：{collection_info.collection_title}\n\n"
            yield f"event: info\ndata: 合集共包含 {collection_info.total_videos} 个视频\n\n"
            yield f"event: info\ndata: 注意：如遇到分P视频，yutto可能会报错停止，这是yutto限制，和本项目无关\n\n"

            async for chunk in run_yutto(command):
                yield chunk
            yield "event: close\ndata: close\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except HTTPException:
        raise
    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="找不到 yutto 命令，请确保已正确安装"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"下载过程出错：{str(e)}"
        )
