import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod
from tkinter import StringVar, Misc


class MQTT_Client:
    def __init__(self, display: Misc, host: str = "localhost", port: int = 1883,
                 topic: str = "carpark/+") -> None:
        self.display = display
        self._config = None
        self.config = (host, port, topic)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value: tuple[str, int, str]):
        host, port, topic = value
        self._config = {"HOST": host, "PORT": port, "TOPIC": topic}

    @staticmethod
    def on_update(client, userdata, message):
        return str(message.payload.decode())

    def update(self, client, userdata, message, sensor):

