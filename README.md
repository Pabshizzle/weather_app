# 🌤 Weather App

**Automated daily weather forecast SMS using Python, AWS Lambda, and Twilio**

> Built by [Pabshizzle](https://github.com/Pabshizzle) — May 2026

---

## What It Does

Every night at 10:30pm (Santiago, Chile time), this bot automatically:

1. Fetches the next day's weather forecast for Santiago from the OpenWeatherMap API
2. Formats a personalized message in Spanish with temperature range, weather description, wind conditions, and rain alert
3. Sends it as an SMS via Twilio

No computer needs to be running. The whole thing lives in the cloud on AWS Lambda, triggered by an EventBridge cron schedule.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Weather Data | OpenWeatherMap Forecast API (free tier) |
| SMS Delivery | Twilio SMS API |
| Cloud Runtime | AWS Lambda (always free tier) |
| Scheduler | Amazon EventBridge (cron trigger) |
| Secret Management | Lambda Environment Variables |
| Key Libraries | requests, twilio, python-dotenv, pytz |

---

## Architecture

```
EventBridge (cron: 02:30 UTC / 10:30pm Santiago)
        ↓
   AWS Lambda
        ↓
  OpenWeatherMap API → filter daytime forecast blocks
        ↓
  Format Spanish message
        ↓
  Twilio SMS → recipient
```

---

## Project Structure

```
weather_app/
    lambda_function.py   # Lambda entry point (handler)
    weather.py           # API call + message formatting
    text_message.py      # Twilio SMS delivery
    requirements.txt     # Python dependencies
    .env                 # Local secrets (not committed)
```

---

## Key Implementation Details

### Timezone Handling
Lambda runs in UTC. To avoid fetching the wrong day's forecast late at night, the bot converts to `America/Santiago` time using `pytz` before calculating tomorrow's date.

### Forecast Filtering
The OpenWeatherMap free tier returns 3-hour forecast blocks. The bot filters to four daytime slots — 09:00, 12:00, 15:00, and 18:00 local time — to build a summary relevant to a working day.

### Wind Conditions
Wind speed is translated into a human-readable comment:
- Under 4 m/s → "Poco viento"
- 4–7 m/s → "Algo de viento, lleva chaqueta"
- Over 7 m/s → "Harto viento, abrígate bien"

### Secret Management
All credentials are stored as Lambda environment variables. The `.env` file is only used for local development and is excluded from the repository via `.gitignore`.

---

## Environment Variables

Set these in Lambda under Configuration → Environment Variables:

| Variable | Description |
|---|---|
| `OPENWEATHER_API_KEY` | API key from openweathermap.org |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `TWILIO_AUTH_TOKEN` | Twilio auth token |
| `TWILIO_FROM` | Twilio phone number (e.g. +1XXXXXXXXXX) |
| `TWILIO_TO` | Recipient phone number (e.g. +56XXXXXXXXX) |

---

## Deployment

Run these steps every time the code is updated:

```bash
# 1. Install dependencies into package folder
pip install --no-user -r requirements.txt -t package

# 2. Copy scripts into package folder
copy lambda_function.py package\
copy weather.py package\
copy text_message.py package\

# 3. Zip from inside the package folder
cd package
python -c "import zipfile, os; zf = zipfile.ZipFile('../weather_app.zip', 'w', zipfile.ZIP_DEFLATED); [zf.write(os.path.join(r,f), os.path.relpath(os.path.join(r,f), '.')) for r,d,files in os.walk('.') for f in files]; zf.close()"
cd ..

# 4. Upload weather_app.zip to Lambda via AWS Console
# 5. Test manually using the Lambda Test tab
# 6. Check CloudWatch logs under the Monitor tab
```

> Never include the `.env` file in the zip.

---

## EventBridge Schedule

```
cron(30 2 * * ? *)
```

Runs every day at 02:30 UTC = 10:30pm Santiago time (UTC-4 in autumn).

---

## Potential Improvements

- Add rain probability threshold for urgent alerts
- Support multiple cities
- Log message history to S3 or DynamoDB
- Add error handling and retry logic for API failures
- Build a Streamlit dashboard to visualise forecast trends
- Migrate to AWS Secrets Manager for production-grade secret management

---

## What I Learned

- REST API consumption and JSON parsing
- Filtering and aggregating data in Python
- Environment variable management for local vs cloud
- AWS Lambda deployment and packaging
- Amazon EventBridge cron scheduling
- Timezone handling with pytz
- Twilio SMS API integration
