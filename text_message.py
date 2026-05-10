from typing import Final
import os
from twilio.rest import Client

def send_sms(message):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    to_number = os.getenv("TWILIO_TO")

    if None in (account_sid, auth_token, from_number, to_number):
        raise ValueError("Missing required Twilio environment variable")

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=from_number,
        to=to_number,#type: ignore
    )