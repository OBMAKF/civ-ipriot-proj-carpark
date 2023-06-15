from broker import Broker
import requests


class TemperatureSensor(Broker):

    API_KEY = '6678d15f045b8d033e4127fdb6071d3b'

    def __init__(self, location) -> None:
        super(TemperatureSensor, self).__init__(
            config_file=f"{location}.toml",
            subscriptions=['update_bays'],
            publishers=['temperature']
        )
        self.url = 'http://api.weatherstack.com/current'
        self.parameters = {'access_key': self.API_KEY, 'query': 'Perth'}
        self.client.connect(self.config['broker_host'], self.config['broker_port'])
        self.client.on_message = self.on_message
        for topic in self.subscriptions:
            self.client.subscribe(f"{self.config['location']}/{topic}")
        self.client.loop_forever()

    def get_temp(self):
        try:
            return requests.get(
                self.url, params=self.parameters
            ).json()['current']['temperature']
        except KeyError:
            # Enter backup API-key (exceeded max calls on free api-key)
            self.parameters['access_key'] = '7230411ea048e2ca7efc23bbf22748fc'
            try:
                return requests.get(
                    self.url,
                    params=self.parameters).json()['current']['temperature']
            except KeyError:
                return "N/A"

    def read_sensor(self) -> str:
        temperature = self.get_temp()

        if temperature.isnumeric():
            return f"{float(temperature):.1f}℃"
        return "N/A"
    
    def on_message(self, client, userdata, message):
        self.client.publish(f"{self.config['location']}/temperature", self.read_sensor())


if __name__ == '__main__':
    x = TemperatureSensor('test')
    print(x.get_temp())
