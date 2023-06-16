# Student:          Nathan Bransby
# Student Number:   V141198

from broker import Broker
import requests


class TemperatureSensor(Broker):
    """Represents a Temperature Sensor.

    This object takes current temperature readings by fetching
    an API request from `http://api.weatherstack.com/current`,
    by default the city is set to Perth.

    Once the current temperature has been called, it then will publish
    it via an MQTT broker.

    :var API_KEY:           The API key required to connect to weatherstack.
    :var API_KEY_BACKUP:    A backup API key for incase the default reaches its maximum call usage.
    :var CITY:              The city that the API requests the location for the current temperature.

    :param location:        The location of the car park, required for setting the config file.
    :param city:            The city that the API requests the location for the current temperature.
    """
    API_KEY = '6678d15f045b8d033e4127fdb6071d3b'
    API_KEY_BACKUP = '7230411ea048e2ca7efc23bbf22748fc'
    CITY = 'Perth'

    def __init__(self, location: str, city: str = 'Perth') -> None:

        super(TemperatureSensor, self).__init__(
            config_file=f"{location}.toml",
            subscriptions=['update_bays'],
            publishers=['temperature']
        )
        self.CITY = city
        self.url = 'http://api.weatherstack.com/current'
        self.parameters = {'access_key': self.API_KEY, 'query': self.CITY}
        self.client.connect(self.config['broker_host'], self.config['broker_port'])
        self.client.on_message = self.on_message

        for topic in self.subscriptions:
            self.client.subscribe(f"{self.config['location']}/{topic}")

        self.client.loop_forever()

    def get_temp(self) -> str | int:
        """Calls the API request.

        :returns:   The JSON results of the API call."""
        try:
            return requests.get(self.url, params=self.parameters).json()['current']['temperature']
        except KeyError:
            # Enter backup API-key (exceeded max calls on free api-key)
            self.parameters['access_key'] = self.API_KEY_BACKUP
            try:
                return requests.get(self.url, params=self.parameters).json()['current']['temperature']
            except KeyError:
                return "N/A"

    def read_sensor(self) -> str:
        """Makes and API request and formats the results."""
        temperature = self.get_temp()

        if type(temperature) is int:
            return f"{float(temperature):.1f}℃"

        return "N/A"
    
    def on_message(self, client, userdata, message):
        self.client.publish(f"{self.config['location']}/temperature", self.read_sensor())
