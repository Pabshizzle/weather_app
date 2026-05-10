from weather import get_weather
from text_message import send_sms

def lambda_handler(event, context):
    message = get_weather()
    send_sms(message)
    return {"status": "Message sent"}


if __name__ == "__main__":
    lambda_handler(None, None)