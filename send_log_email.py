import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
from datetime import date

# 邮件配置信息
sender_email = 'xxxxxxxxxx@qq.com'  # 发件人QQ邮箱
receiver_email = 'xxxxxxxxxx@qq.com'  # 收件人邮箱
smtp_server = 'smtp.qq.com'  # QQ邮箱的SMTP服务器地址
smtp_port = 465  # SMTP SSL端口号
smtp_password = 'xxxxxxxxxxxxxxxx'  # 发件人邮箱的授权码

# 获取日志文件路径
def get_latest_log():
    log_dir = '/www/wwwroot/python/logs'
    today = date.today()  # 使用 datetime 的 date 获取当前日期
    year_month_dir = os.path.join(log_dir, f"{today.year}/{today.month:02d}")  # 当前年和月的目录
    log_file = os.path.join(year_month_dir, f"{today.day:02d}.log")  # 当前日志文件
    if os.path.exists(log_file):
        return log_file
    else:
        return None

# 发送邮件函数
def send_log_email(log_file):
    # 创建邮件对象
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = Header('脚本运行日志', 'utf-8')

    # 添加邮件正文
    if log_file:
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        message.attach(MIMEText(log_content, 'plain', 'utf-8'))
    else:
        message.attach(MIMEText("未找到日志文件。", 'plain', 'utf-8'))

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, smtp_password)
        server.sendmail(sender_email, [receiver_email], message.as_string())
        server.quit()
        print(f"日志邮件发送成功：{log_file if log_file else '测试邮件'}")
    except Exception as e:
        print(f"发送邮件失败: {e}")

# 主函数
if __name__ == '__main__':
    log_file = get_latest_log()
    send_log_email(log_file)  # 无论是否有日志文件，都发送邮件
