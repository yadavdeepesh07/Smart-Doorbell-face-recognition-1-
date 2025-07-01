import os
from twilio.rest import Client
from app.config import get_env

def send_sms_alert(name, confidence):
    account_sid = get_env("TWILIO_ACCOUNT_SID")
    auth_token = get_env("TWILIO_AUTH_TOKEN")
    from_number = get_env("TWILIO_PHONE")
    to_number = get_env("USER_PHONE")

    client = Client(account_sid, auth_token)

    body = f"🚨 {name} is at your door! Confidence: {confidence:.2f}%"
    message = client.messages.create(
        body=body,
        from_=from_number,
        to=to_number
    )
    print("📲 SMS sent:", message.sid)
