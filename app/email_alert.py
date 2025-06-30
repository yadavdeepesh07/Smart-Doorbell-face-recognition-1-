import smtplib, os
from email.message import EmailMessage

def send_email_alert(subject, body):
    if os.getenv("ENABLE_EMAIL") != "True":
        return
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = os.getenv("EMAIL_ADDRESS")
    msg['To'] = os.getenv("EMAIL_ADDRESS")
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
