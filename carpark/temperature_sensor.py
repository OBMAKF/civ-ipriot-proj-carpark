from config_manager import ConfigManager
from sensor import Sensor
from datetime import datetime
import requests


class TemperatureSensor(Sensor):
    API_KEY = '7230411ea048e2ca7efc23bbf22748fc'

    def __init__(self, carpark) -> None:
        self.carpark = carpark
        self.url = 'http://api.weatherstack.com/current'
        self.parameters = {'access_key': self.API_KEY, 'query': 'Perth'}

    def get_temp(self):
        return requests.get(
            self.url, params=self.parameters
        ).json()['current']['temperature']

    def read_sensor(self):
        date = str(datetime.now().strftime('%d-%m-%Y'))
        time = datetime.now().strftime('%H:%M:%S')
        temperature = self.get_temp()

        return {'date': date, 'time': time,
                'temperature': f"{float(temperature):.2f}℃"}


if __name__ == '__main__':
    x = TemperatureSensor(None)
    print(x.read_sensor())
