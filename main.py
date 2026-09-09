import os
import requests

# Load environment variables
api_key = os.environ.get("OWM_API_KEY")
bot_token = os.environ.get("TEL_BOT_TOKEN")
bot_chat_id = os.environ.get("TEL_CHAT_ID")

# Weather API call
weather_url = "http://api.openweathermap.org/data/2.5/forecast"
parameters = {
    "lat": 25.5167,
    "lon": 77.2333,
    "units": "metric",
    "appid": api_key,
    "cnt": 4,
    "lang": "en",
}

response = requests.get(weather_url, params=parameters)
response.raise_for_status()
data = response.json()


def it_will_rain(report: dict) -> bool:
    """Check if weather code in forecast list indicates rain/snow/drizzle (< 600)."""
    for hour_data in report.get("list", []):
        weather_id = int(hour_data["weather"][0]["id"])
        if weather_id < 600:
            return True
    return False


def telegram_bot_sendtext(bot_message: str):
    if not bot_token or not bot_chat_id:
        print("Error: TEL_BOT_TOKEN or TEL_CHAT_ID environment variable is missing.")
        return None

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": bot_chat_id,
        "text": bot_message,
    }

    # Optional: Include proxy ONLY if running on PythonAnywhere free tier
    # proxies = {"http": "http://proxy.server:3128", "https": "http://proxy.server:3128"}

    try:
        # Pass params=payload to safely URL-encode the message text
        response = requests.get(url, params=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred while sending Telegram message: {e}")
        return None


# Execute notification
if it_will_rain(data):
    print("Rain forecast detected. Sending Telegram message...")
    telegram_bot_sendtext("Carry an Umbrella ☔")
else:
    print("No rain detected in the forecast.")
    telegram_bot_sendtext("No need to carry an Umbrella ☀️")
