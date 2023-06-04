import paho.mqtt.client as mqtt
from config_manager import ConfigManager
from tomli import load
from display import TkDisplay
from temp_sensor import TemperatureSensor
from time import sleep
from datetime import datetime


class CarPark:
    TOTAL_SPACES = 0
    BROKER = 'localhost'
    PORT = 1883
    TOPIC = None

    def __init__(self, config_file):
        with ConfigManager(config_file) as config:
            config = load(config)['config']
            self.BROKER = config['broker_host']
            self.PORT = config['broker_port']
            self.TOPIC = config['location']
            self.TOTAL_SPACES = config['total_spaces']

        self.sensor = TemperatureSensor(self)

        self.client = mqtt.Client()
        self.client.connect(self.BROKER, self.PORT)
        self.count = 0
        self.display = TkDisplay(config_file, self)

    def assign_car(self):
        if self.count < self.TOTAL_SPACES:
            self.count += 1
            self.publish()

    def pay_fee(self):
        if 1 <= self.count:
            self.count -= 1
            self.publish()

    def publish(self):
            self.client.publish(
                self.TOPIC,
                f"{self.sensor.read_sensor()['temperature']}\n" +
                f"Free Bays: {self.free_bays()}")

    def free_bays(self) -> int:
        return self.TOTAL_SPACES - self.count


if __name__ == '__main__':
    async def main():
        connections = []
    park = CarPark('test.toml')