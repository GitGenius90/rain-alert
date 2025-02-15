import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWM_API_KEY")  # generate from api.openweathermap.org
account_sid = "YOUR ACCOUNT SID"  # Twilio Account SID
auth_token = os.environ.get("AUTH_TOKEN")  # Twilio Account Token

weather_params = {
    "lat": 49.282730,  # Vancouver's latitude and longitude
    "lon": -123.120735,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    NUMBERS = {
        "Name_1": "YOUR TWILIO VERIFIED REAL NUMBER",
        "Name_2": "YOUR TWILIO VERIFIED REAL NUMBER",
    }
    twilioNumber = "YOUR TWILIO VIRTUAL NUMBER"
    client = Client(account_sid, auth_token, http_client=proxy_client)
    for name, number in NUMBERS.items():
        message = client.messages \
            .create(
            body=f'Morning {name}! It\'s going to rain today. Remember to bring an ☔️ and stay dry.',
            from_=twilioNumber,
            to=number)
        print(message.status)
