from typing import Any, Optional
from fastapi import APIRouter, Body, HTTPException, Request
from pydantic import BaseModel, EmailStr
import yaml
import os
import re
from scripts.utils import load_config
from scripts.send_log_email import send_email

router = APIRouter()

def get_config_path():
    """获取配置文件路径"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'config', 'config.yaml')

def get_mcp_skill_path():
    """获取MCP配套skill文件路径"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'skills', 'bilibili-history-mcp', 'SKILL.md')

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
    pattern = f"^{indent}{re.escape(field)}:.*$"
    
    # 处理多行内容
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.MULTILINE):
            if new_value is None or new_value == "":
                lines[i] = f"{indent}{field}:"  # 设置为空值
            else:
                lines[i] = f"{indent}{field}: {new_value}"
            break
    else:
        # 如果字段不存在且传入了有效值，则插入到父级 YAML 节点末尾。
        # 这用于为旧配置文件补充新增字段，例如 email.auth_username。
        if new_value is None or new_value == "":
            return content

        new_line = f"{indent}{field}: {new_value}"

        if len(field_path) == 1:
            lines.append(new_line)
        else:
            parent_indent = ' ' * (2 * (len(field_path) - 2))
            parent_field = field_path[-2]
            parent_pattern = f"^{parent_indent}{re.escape(parent_field)}:.*$"

            for parent_index, line in enumerate(lines):
                if re.match(parent_pattern, line, re.MULTILINE):
                    insert_index = parent_index + 1
                    while insert_index < len(lines):
                        current_line = lines[insert_index]
                        if current_line.strip() == "":
                            break
                        current_indent = len(current_line) - len(current_line.lstrip(' '))
                        if current_indent <= len(parent_indent):
                            break
                        insert_index += 1
                    lines.insert(insert_index, new_line)
                    break
            else:
                lines.append(new_line)
    
    return '\n'.join(lines)

class EmailConfig(BaseModel):
    """邮件配置模型"""
    smtp_server: Optional[str] = None
    smtp_port: Optional[int] = None
    sender: Optional[EmailStr] = None
    auth_username: Optional[str] = None
    password: Optional[str] = None
    receiver: Optional[EmailStr] = None

class TestEmailRequest(BaseModel):
    """测试邮件请求模型"""
    to_email: Optional[EmailStr] = None  # 可选，如果为空则使用配置中的接收者邮箱
    subject: str = "测试邮件"
    content: str = "这是一封测试邮件，用于验证邮箱配置是否有效。"

class McpConfigUpdate(BaseModel):
    """MCP配置更新模型"""
    enabled: bool

def normalize_mcp_path(path: Optional[str]) -> str:
    """规范化MCP挂载路径"""
    normalized = (path or "/mcp").strip()
    if not normalized.startswith("/"):
        normalized = f"/{normalized}"
    if len(normalized) > 1:
        normalized = normalized.rstrip("/")
    return normalized or "/mcp"

def build_server_url(request: Request, server_config: dict[str, Any]) -> str:
    """优先使用当前请求来源生成客户端可访问地址。"""
    request_origin = str(request.base_url).rstrip("/")
    if request_origin:
        return request_origin

    scheme = "https" if server_config.get("ssl_enabled") else "http"
    host = server_config.get("host") or "127.0.0.1"
    if host in {"0.0.0.0", "::", "[::]"}:
        host = "127.0.0.1"

    port = int(server_config.get("port", 8899))
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    return f"{scheme}://{host}:{port}"

def build_mcp_config_response(
    config: dict[str, Any],
    request: Request,
    restart_required: bool = False
) -> dict[str, Any]:
    """构造前端设置页需要的MCP配置。"""
    server_config = config.get("server", {}) or {}
    mcp_config = server_config.get("mcp", {}) or {}
    path = normalize_mcp_path(mcp_config.get("path", "/mcp"))
    server_url = build_server_url(request, server_config)
    mcp_url = f"{server_url}{path if path == '/' else path + '/'}"
    token = os.environ.get("BHF_MCP_TOKEN") or mcp_config.get("token")
    skill_content = ""
    skill_path = get_mcp_skill_path()
    if os.path.exists(skill_path):
        with open(skill_path, 'r', encoding='utf-8') as f:
            skill_content = f.read()

    return {
        "status": "success",
        "enabled": bool(mcp_config.get("enabled", False)),
        "path": path,
        "auth_enabled": bool(mcp_config.get("auth_enabled", True)),
        "token": token or "",
        "token_configured": bool(token),
        "max_page_size": int(mcp_config.get("max_page_size", 100)),
        "server_url": server_url,
        "mcp_url": mcp_url,
        "skill_content": skill_content,
        "restart_required": restart_required
    }

def get_line_indent(line: str) -> int:
    """获取YAML行缩进宽度。"""
    return len(line) - len(line.lstrip(" "))

def is_yaml_key(line: str, key: str, indent: Optional[int] = None) -> bool:
    """判断某行是否为指定缩进层级的YAML键。"""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return False
    if indent is not None and get_line_indent(line) != indent:
        return False
    return bool(re.match(rf"^{re.escape(key)}\s*:", stripped))

def find_block_end(lines: list[str], start_index: int, parent_indent: int) -> int:
    """查找YAML块结束位置，返回可插入的行下标。"""
    for index in range(start_index + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped and get_line_indent(lines[index]) <= parent_indent:
            return index
    return len(lines)

def update_mcp_enabled_field(content: str, enabled: bool) -> str:
    """只更新server.mcp.enabled，尽量保持配置文件其他内容不变。"""
    enabled_value = str(enabled).lower()
    lines = content.split("\n")

    server_index = next((i for i, line in enumerate(lines) if is_yaml_key(line, "server", 0)), None)
    if server_index is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["server:", "  mcp:", f"    enabled: {enabled_value}"])
        return "\n".join(lines)

    server_indent = get_line_indent(lines[server_index])
    server_end = find_block_end(lines, server_index, server_indent)
    mcp_indent = server_indent + 2
    enabled_indent = mcp_indent + 2

    mcp_index = next(
        (i for i in range(server_index + 1, server_end) if is_yaml_key(lines[i], "mcp", mcp_indent)),
        None
    )
    if mcp_index is None:
        lines.insert(server_end, f"{' ' * mcp_indent}mcp:")
        lines.insert(server_end + 1, f"{' ' * enabled_indent}enabled: {enabled_value}")
        return "\n".join(lines)

    mcp_end = find_block_end(lines, mcp_index, mcp_indent)
    enabled_index = next(
        (i for i in range(mcp_index + 1, mcp_end) if is_yaml_key(lines[i], "enabled", enabled_indent)),
        None
    )
    if enabled_index is None:
        lines.insert(mcp_index + 1, f"{' ' * enabled_indent}enabled: {enabled_value}")
    else:
        current_indent = lines[enabled_index][:get_line_indent(lines[enabled_index])]
        lines[enabled_index] = f"{current_indent}enabled: {enabled_value}"

    return "\n".join(lines)

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
            "auth_username": email_config.get('auth_username') or email_config.get('username'),
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
    request: Request,
    smtp_server: Optional[str] = Body(default=...),
    smtp_port: Optional[int] = Body(default=...),
    sender: Optional[str] = Body(default=...),  # 改为str类型以接受空字符串
    auth_username: Optional[str] = Body(default=None),
    password: Optional[str] = Body(default=...),
    receiver: Optional[str] = Body(default=...)  # 改为str类型以接受空字符串
):
    """
    更新邮件配置
    
    - **smtp_server**: SMTP服务器地址，可以为空
    - **smtp_port**: SMTP服务器端口，可以为空
    - **sender**: 发件人邮箱，可以为空
    - **auth_username**: SMTP认证用户名，可选；为空则使用发件人邮箱
    - **password**: 邮箱授权码，可以为空
    - **receiver**: 收件人邮箱，可以为空
    """
    try:
        request_body = await request.json()

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

        if 'auth_username' in request_body:
            value = f'"{auth_username}"' if auth_username else None
            content = update_yaml_field(content, ['email', 'auth_username'], value)
            email_config['auth_username'] = auth_username
            
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
                "auth_username": email_config.get('auth_username') or email_config.get('username'),
                "receiver": email_config.get('receiver'),
                "password": email_config.get('password')  # 返回明文密码
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新邮件配置失败: {str(e)}"
        )

@router.post("/test-email", summary="发送测试邮件")
async def send_test_email(request: TestEmailRequest):
    """
    发送测试邮件以验证邮箱配置是否有效
    
    - **to_email**: 收件人邮箱，可选，如果为空则使用配置中的收件人
    - **subject**: 邮件主题，默认为"测试邮件"
    - **content**: 邮件内容，默认为"这是一封测试邮件，用于验证邮箱配置是否有效。"
    
    返回:
    - **status**: 发送状态，"success"或"error"
    - **message**: 状态描述信息
    """
    try:
        # 获取当前邮件配置
        config = load_config()
        email_config = config.get('email', {})
        
        # 检查邮件配置是否完整
        if not all([
            email_config.get('smtp_server'),
            email_config.get('smtp_port'),
            email_config.get('sender'),
            email_config.get('password'),
            request.to_email or email_config.get('receiver')
        ]):
            raise ValueError("邮件配置不完整，请先完善邮件配置")
        
        # 发送测试邮件
        result = await send_email(
            subject=request.subject,
            content=request.content,
            to_email=request.to_email
        )
        
        return result
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"发送测试邮件失败: {str(e)}"
        )

@router.get("/mcp-config", summary="获取MCP配置")
async def get_mcp_config(request: Request):
    """获取当前MCP配置，供前端设置页生成连接提示词。"""
    try:
        config = load_config()
        return build_mcp_config_response(config, request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取MCP配置失败: {str(e)}"
        )

@router.post("/mcp-config", summary="更新MCP开关配置")
async def update_mcp_config(request_data: McpConfigUpdate, request: Request):
    """
    更新MCP启用状态。

    MCP请求会实时读取配置，因此开关保存后立即生效。
    """
    try:
        config_path = get_config_path()
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            config = yaml.safe_load(content) or {}

        server_config = config.setdefault("server", {})
        mcp_config = server_config.setdefault("mcp", {})
        updated_content = update_mcp_enabled_field(content, request_data.enabled)
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        mcp_config["enabled"] = request_data.enabled
        response = build_mcp_config_response(
            config,
            request,
            restart_required=False
        )
        response["message"] = "MCP配置已更新"
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新MCP配置失败: {str(e)}"
        )
