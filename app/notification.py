import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import get_env

def send_email_notification(subject, body, to_email):
    if get_env("ENABLE_EMAIL", "false").lower() != "true":
        return
    msg = MIMEMultipart()
    msg['From'] = get_env("EMAIL_ADDRESS")
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(get_env("EMAIL_ADDRESS"), get_env("EMAIL_PASSWORD"))
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        print("Email sent.")
    except Exception as e:
        print("Email failed:", e)
