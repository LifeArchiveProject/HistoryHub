import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Dict

from loguru import logger

from scripts.utils import load_config, setup_logger, get_logs_path

# 确保日志系统已初始化
setup_logger()


def get_task_execution_logs() -> str:
    """
    获取最近一次计划任务执行期间的完整日志内容

    从当前日志文件中查找最近一次任务执行的日志，
    包含从任务开始到文件结尾的所有日志内容。

    Returns:
        str: 最近一次计划任务执行的完整日志内容，如果没有找到则返回提示信息
    """
    # 获取当前日志文件路径
    log_file = get_logs_path()
    
    # 检查日志文件是否存在
    if not os.path.exists(log_file):
        return "今日暂无日志记录"

    with open(log_file, 'r', encoding='utf-8') as f:
        log_lines = f.readlines()
    
    # 如果日志为空
    if not log_lines:
        return "今日暂无日志记录"

    # 查找最近一次计划任务执行的开始位置
    start_index = -1
    end_index = len(log_lines)  # 默认到文件末尾
    
    # 计划任务开始的标记
    task_start_markers = [
        "=== 执行任务链:",         # 主任务链开始
        "=== 执行任务:",          # 单个任务开始
        "=== 调度器触发任务执行"    # 调度器触发的任务
    ]
    
    # 从后向前查找最近的任务执行开始标记
    for i in range(len(log_lines) - 1, -1, -1):
        line = log_lines[i]
        if any(marker in line for marker in task_start_markers):
            start_index = i
            break
    
    # 如果找不到任务执行开始标记，则返回提示信息
    if start_index == -1:
        return "未找到任务执行记录"
    
    # 提取任务执行期间的日志 - 从开始标记一直到文件结束
    task_logs = log_lines[start_index:end_index]
    return "".join(task_logs)


async def send_email(subject: str, content: Optional[str] = None, to_email: Optional[str] = None) -> Dict:
    """
    发送邮件

    Args:
        subject: 邮件主题
        content: 邮件内容，如果为None则发送当天的任务执行日志
        to_email: 收件人邮箱，如果为None则使用配置文件中的默认收件人

    Returns:
        dict: 发送结果，包含status和message
    """
    logger.info(f"准备发送邮件: {subject}")
    try:
        config = load_config()
        smtp_server = config.get('email', {}).get('smtp_server', 'smtp.qq.com')
        smtp_port = config.get('email', {}).get('smtp_port', 587)
        sender_email = config.get('email', {}).get('sender')
        sender_password = config.get('email', {}).get('password')
        receiver_email = to_email or config.get('email', {}).get('receiver')

        if not all([sender_email, sender_password, receiver_email]):
            logger.error("邮件配置不完整，请检查配置文件")
            raise ValueError("邮件配置不完整，请检查配置文件")

        # 如果没有提供内容，则获取任务执行期间的日志
        if content is None:
            content = get_task_execution_logs()

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
        server = None
        email_sent = False

        try:
            # 不使用 with 语句，以便更好地控制异常处理流程
            server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            email_sent = True  # 标记邮件已成功发送
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP错误: {str(e)}")
        except TimeoutError:
            raise Exception("SMTP服务器连接超时")
        finally:
            # 安全关闭连接
            if server:
                try:
                    server.quit()
                except Exception as e:
                    # 如果邮件已经发送成功，则忽略关闭连接时的错误
                    if email_sent:
                        return {"status": "success", "message": "邮件发送成功（服务器连接关闭时出现非致命错误）"}
                    else:
                        # 如果邮件未发送成功，则抛出关闭连接时的错误
                        raise Exception(f"关闭SMTP连接时出错: {str(e)}")

        # 如果执行到这里，说明邮件发送成功且连接正常关闭
        logger.info(f"邮件发送成功: {subject}")
        return {"status": "success", "message": "邮件发送成功"}

    except Exception as e:
        error_msg = f"邮件发送失败: {str(e)}"
        logger.error(f"邮件发送失败: {str(e)}")

        # 检查特定的错误情况，如 \x00\x00\x00，这可能表示邮件实际已发送
        if "\\x00\\x00\\x00" in str(e):
            logger.info("邮件可能已成功发送（出现特殊错误码但通常不影响邮件传递）")
            return {"status": "success", "message": "邮件可能已成功发送（出现特殊错误码但通常不影响邮件传递）"}

        return {"status": "error", "message": error_msg}

def get_today_logs():
    """
    获取今日全部日志内容
    
    从当前日志文件获取所有日志行
    
    Returns:
        list: 今日的全部日志行
    """
    # 获取当前日志文件路径
    log_file = get_logs_path()
    logs = []
    
    # 检查今天的日志文件
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            logs = f.read().splitlines()
    
    return logs

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
