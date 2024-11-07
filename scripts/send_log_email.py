import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from scripts.utils import load_config, get_logs_path


async def send_email(subject: str, content: Optional[str] = None, to_email: Optional[str] = None):
    """
    发送邮件
    
    Args:
        subject: 邮件主题
        content: 邮件内容，如果为None则发送当天的日志内容
        to_email: 收件人邮箱，如果为None则使用配置文件中的默认收件人
    
    Returns:
        dict: 发送结果，包含status和message
    """
    try:
        config = load_config()
        smtp_server = config.get('email', {}).get('smtp_server', 'smtp.qq.com')
        smtp_port = config.get('email', {}).get('smtp_port', 587)
        sender_email = config.get('email', {}).get('sender')
        sender_password = config.get('email', {}).get('password')
        receiver_email = to_email or config.get('email', {}).get('receiver')
        
        if not all([sender_email, sender_password, receiver_email]):
            raise ValueError("邮件配置不完整，请检查配置文件")
        
        # 如果没有提供内容，则读取当天的日志文件
        if content is None:
            log_file = get_logs_path()
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "今日暂无日志记录"

        # 格式化主题（替换时间占位符）
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subject = subject.format(current_time=current_time)

        # 创建邮件对象
        message = MIMEMultipart()
        message['From'] = Header(sender_email)
        message['To'] = Header(receiver_email)
        message['Subject'] = Header(subject)
        
        # 添加邮件内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 连接SMTP服务器并发送
        try:
            with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
                return {"status": "success", "message": "邮件发送成功"}
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP错误: {str(e)}")
        except TimeoutError:
            raise Exception("SMTP服务器连接超时")
        
    except Exception as e:
        error_msg = f"邮件发送失败: {str(e)}"
        return {"status": "error", "message": error_msg}

# 测试代码
if __name__ == '__main__':
    import asyncio
    
    async def test_send():
        try:
            await send_email(
                subject="测试日志邮件",
                content=None  # 测试发送当天的日志
            )
            print("测试邮件发送成功")
        except Exception as e:
            print(f"测试邮件发送失败: {e}")
    
    asyncio.run(test_send())
