import requests
from datetime import datetime, time

class Weather:
    def __init__(self):
        self.current_temperature = None
        self.sunrise_time = None
        self.sunset_time = None
        self.overcast = None
        self.refresh()

    def refresh(self):
        api_url = "https://api.open-meteo.com/v1/forecast?latitude=45.8144&longitude=15.978&current=temperature_2m,weathercode&daily=sunrise,sunset&timezone=auto&forecast_days=1"

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            current_weather = data.get('current', {}) 
            self.current_temperature = current_weather.get('temperature_2m', None)
            current_weathercode = current_weather.get('weathercode', None) 
            daily_weather = data.get('daily', {})
            sunrise = daily_weather.get('sunrise', [None])[0].split('T')[1]
            sunset = daily_weather.get('sunset', [None])[0].split('T')[1]
            self.sunrise_time = datetime.strptime(sunrise, "%H:%M").time()
            self.sunset_time = datetime.strptime(sunset, "%H:%M").time()
            if current_weathercode == 0 or current_weathercode == 1 or current_weathercode == 2 or current_weathercode == 3:
                self.overcast = False
            else:
                self.overcast = True
        else:
            print(f"Error code {response.status_code}")
