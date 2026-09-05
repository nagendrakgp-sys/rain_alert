import os
import requests

api_key = os.environ.get("OWM_API_KEY")
weather_url = "http://api.openweathermap.org/data/3.3/forecast"
parameters = {
    "lat": 25.5167,
    "lon": 77.2333,
    "units": "metric",
    "appid" : api_key,
    "cnt" : 4,
    "lang" : "en"
}

response = requests.get(weather_url, params=parameters)
response.raise_for_status()
data = response.json()


def it_will_rain(report: dict):
    for hour_data in report["list"]:
        weather_id = int(hour_data['weather'][0]['id'])
        if weather_id < 600:
            return True
    return False

def telegram_bot_sendtext(bot_message):
    bot_token = os.environ.get("TEL_BOT_TOKEN")
    bot_chat_id = os.environ.get("TEL_CHAT_ID")

    # ⚠️ Check this line closely! It must use f' and contain api.telegram.org/bot
    send_text = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+bot_chat_id+'&text='+bot_message

    proxies = {
        'http': 'http://proxy.server:3128',
        'https': 'http://proxy.server:3128',
    }

    try:
        response = requests.get(send_text, proxies=proxies)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if it_will_rain(data):
    print("Rain forecast detected. Sending Telegram message...")
    telegram_bot_sendtext("k")
else:
    print("No rain detected in the current 4-block forecast.")
