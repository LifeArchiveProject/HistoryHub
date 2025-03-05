from typing import Optional
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, EmailStr
import yaml
import os
import re
from scripts.utils import load_config

router = APIRouter()

def get_config_path():
    """获取配置文件路径"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'config', 'config.yaml')

def update_yaml_field(content: str, field_path: list, new_value: Optional[str]) -> str:
    """
    更新YAML文件中特定字段的值，保持其他内容不变
    
    Args:
        content: YAML文件内容
        field_path: 字段路径，如 ['email', 'smtp_server']
        new_value: 新的值，如果为None则删除该字段
    """
    # 构建YAML路径的正则表达式
    indent = ' ' * (2 * (len(field_path) - 1))  # YAML标准缩进
    field = field_path[-1]
    pattern = f"^{indent}{field}:.*$"
    
    # 处理多行内容
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.MULTILINE):
            if new_value is None or new_value == "":
                lines[i] = f"{indent}{field}:"  # 设置为空值
            else:
                lines[i] = f"{indent}{field}: {new_value}"
            break
    
    return '\n'.join(lines)

class EmailConfig(BaseModel):
    """邮件配置模型"""
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    sender: Optional[EmailStr] = None
    password: Optional[str] = None
    receiver: Optional[EmailStr] = None

@router.get("/email-config", summary="获取邮件配置")
async def get_email_config():
    """获取当前邮件配置"""
    try:
        config = load_config()
        email_config = config.get('email', {})
        return {
            "smtp_server": email_config.get('smtp_server'),
            "smtp_port": email_config.get('smtp_port'),
            "sender": email_config.get('sender'),
            "receiver": email_config.get('receiver'),
            "password": email_config.get('password')  # 返回明文密码
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取邮件配置失败: {str(e)}"
        )

@router.post("/email-config", summary="更新邮件配置")
async def update_email_config(
    smtp_server: Optional[str] = Body(default=...),
    smtp_port: Optional[int] = Body(default=...),
    sender: Optional[str] = Body(default=...),  # 改为str类型以接受空字符串
    password: Optional[str] = Body(default=...),
    receiver: Optional[str] = Body(default=...)  # 改为str类型以接受空字符串
):
    """
    更新邮件配置
    
    - **smtp_server**: SMTP服务器地址，可以为空
    - **smtp_port**: SMTP服务器端口，可以为空
    - **sender**: 发件人邮箱，可以为空
    - **password**: 邮箱授权码，可以为空
    - **receiver**: 收件人邮箱，可以为空
    """
    try:
        # 读取当前配置文件内容
        config_path = get_config_path()
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            config = yaml.safe_load(content)  # 仅用于获取当前配置
        
        # 获取当前邮件配置
        email_config = config.get('email', {})
        
        # 逐个更新配置字段
        if smtp_server is not ...:  # 检查是否提供了该参数
            value = f'"{smtp_server}"' if smtp_server else None
            content = update_yaml_field(content, ['email', 'smtp_server'], value)
            email_config['smtp_server'] = smtp_server
            
        if smtp_port is not ...:
            value = str(smtp_port) if smtp_port is not None else None
            content = update_yaml_field(content, ['email', 'smtp_port'], value)
            email_config['smtp_port'] = smtp_port
            
        if sender is not ...:
            value = f'"{sender}"' if sender else None
            content = update_yaml_field(content, ['email', 'sender'], value)
            email_config['sender'] = sender
            
        if password is not ...:
            value = f'"{password}"' if password else None
            content = update_yaml_field(content, ['email', 'password'], value)
            email_config['password'] = password
            
        if receiver is not ...:
            value = f'"{receiver}"' if receiver else None
            content = update_yaml_field(content, ['email', 'receiver'], value)
            email_config['receiver'] = receiver
        
        # 写回配置文件
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "message": "邮件配置更新成功",
            "config": {
                "smtp_server": email_config.get('smtp_server'),
                "smtp_port": email_config.get('smtp_port'),
                "sender": email_config.get('sender'),
                "receiver": email_config.get('receiver'),
                "password": email_config.get('password')  # 返回明文密码
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新邮件配置失败: {str(e)}"
        ) 