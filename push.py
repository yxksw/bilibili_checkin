import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger

def format_email_message(all_results):
    html_content = ["<html><body>"]
    html_content.append("<h2>Bilibili 任务报告</h2>")

    for result in all_results:
        user_info = result.get('user_info')
        if user_info:
            account_name = user_info['uname']
            html_content.append(f"<hr><h3>账号: {account_name} (Lv.{user_info['level_info']['current_level']})</h3>")
        else:
            account_name = f"账号 {result['account_index']}"
            html_content.append(f"<hr><h3>{account_name}</h3>")

        html_content.append("<ul>")
        for name, (success, message) in result['tasks'].items():
            status_icon = "✅" if success else "❌"
            reason = f" - {message}" if message else ""
            html_content.append(f"<li><strong>{name}</strong>: {status_icon}{reason}</li>")

        if user_info:
            html_content.append(f"<li><strong>硬币余额</strong>: {user_info['money']}</li>")
        html_content.append("</ul>")

    beijing_time = datetime.now(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S')
    html_content.append(f"<p><em>报告时间: {beijing_time}</em></p>")
    html_content.append("</body></html>")

    return "\n".join(html_content)

def send_email(smtp_host, smtp_port, smtp_user, smtp_pass, sender_email, receiver_email, title, content):
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender_email
        msg['To'] = receiver_email

        msg.attach(MIMEText(content, 'html', 'utf-8'))

        with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_pass)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        logger.info('邮件发送成功！')
    except Exception as e:
        logger.error(f'邮件发送失败: {e}')