import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
from datetime import date
from scripts.utils import load_config

config = load_config()

def get_latest_log():
    log_dir = config['log_folder']
    today = date.today()
    year_month_dir = os.path.join(log_dir, f"{today.year}/{today.month:02d}")
    log_file = os.path.join(year_month_dir, f"{today.day:02d}.log")
    if os.path.exists(log_file):
        return log_file
    else:
        return None

def send_log_email(log_file=None):
    message = MIMEMultipart()
    message['From'] = config['email']['sender']
    message['To'] = config['email']['receiver']
    message['Subject'] = Header('脚本运行日志', 'utf-8')

    if log_file:
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        message.attach(MIMEText(log_content, 'plain', 'utf-8'))
    else:
        message.attach(MIMEText("未找到日志文件。", 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL(config['email']['smtp_server'], config['email']['smtp_port'])
        server.login(config['email']['sender'], config['email']['password'])
        server.sendmail(config['email']['sender'], [config['email']['receiver']], message.as_string())
        server.quit()
        return {"status": "success", "message": f"日志邮件发送成功：{log_file if log_file else '测试邮件'}"}
    except Exception as e:
        return {"status": "error", "message": f"发送邮件失败: {e}"}

def send_latest_log():
    log_file = get_latest_log()
    return send_log_email(log_file)

if __name__ == '__main__':
    result = send_latest_log()
    print(result["message"])
