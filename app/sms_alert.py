from twilio.rest import Client
import os

def send_sms_alert(body):
    if os.getenv("ENABLE_SMS") != "True":
        return
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        body=body,
        from_=os.getenv("TWILIO_PHONE"),
        to=os.getenv("USER_PHONE")
    )
