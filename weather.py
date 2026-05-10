import requests
import os
import sys
import locale
import pytz
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
from datetime import datetime, timedelta
sys.stdout.reconfigure(encoding='utf-8') #type: ignore
from dotenv import load_dotenv

load_dotenv()

def get_weather():
    
    santiago_tz = pytz.timezone('America/Santiago')
    now_santiago = datetime.now(santiago_tz)
    tomorrow = (now_santiago + timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow_date = (now_santiago + timedelta(days=1)).strftime('%A, %d de %B de %Y')
    
    target_times = ["09:00:00", "12:00:00", "15:00:00", "18:00:00"]
    temps = []
    descriptions = []
    winds = []
    rain = False

    api_key = os.getenv('OPENWEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/forecast?q=Santiago,CL&appid={api_key}&units=metric&lang=es'

    response = requests.get(url)
    data = response.json()

    for block in data["list"]:
        if block["dt_txt"].startswith(tomorrow):
            time = block["dt_txt"].split(" ")[1]
            if time in target_times:
                temps.append(block["main"]["temp"])
                descriptions.append(block["weather"][0]["description"])
                winds.append(block["wind"]["speed"])
                if "rain" in block:
                    rain = True

    if max(winds) < 4:
        wind_comment = "Poco viento 🍃"
    elif max(winds) < 7:
        wind_comment = "Algo de viento, lleva chaqueta 🌬️"
    else:
        wind_comment = "Harto viento, abrígate bien 💨"

    message = (
        f"🌤 Buenos días mi Catita bella!\n"
        f"El tiempo de mañana {tomorrow_date} en Santiago:\n\n"
        f"🌡 Temperatura: {min(temps)}°C a {max(temps)}°C\n"
        f"🌥 {descriptions[1].capitalize()}\n"
        f"💨 {wind_comment}\n"
        f"🌧 Lluvia: {'Sí, lleva paraguas babe' if rain else 'No, sin lluvia'}\n\n"
        f"Espero que tengas un lindo día, mi amor🩷\n"
        f"Pablo, Bodoque, y Jupita. 🐾"
    )

    return message