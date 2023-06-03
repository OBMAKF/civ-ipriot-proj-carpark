import paho.mqtt.client as mqtt
from abc import ABC, abstractmethod
from tkinter import StringVar, Misc


class MQTT_Client:
    HOST = None
    PORT = None
    TOPICS = []

    def __init__(self, display: Misc, topics: list[str], host: str = "localhost",
                 port: int = 1883, ) -> None:
        super(MQTT_Client, self).__init__()
        self.display = display
        self._config = None
        self.config = (host, port, topics)
        self.client = mqtt.Client()
        self.cliet.on_message = self.on_message

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __str__(self) -> str:
        return f"MQTT Connection: {self.TOPICS}:{self.PORT}"

    def __call__(self, topic, message):
        self.publish(topic, message)

    def connect(self):
        self.client.connect(self.HOST, self.PORT)
        self.client.loop_start()
        # todo start loop here...

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def publish(self, message: str, topic: str):
        self.client.publish(topic, message)

    def subscribe(self, topic: str):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, message):
        for topic in self.TOPICS:
            if message.topic == topic:
                self.display.update_display(message.payload.decode(), topic)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value: tuple[str, int, list[str]]):
        host, port, topics = value
        self.HOST = host
        self.PORT = port
        self.TOPICS = topics
        self._config = {"HOST": host, "PORT": port, "TOPICS": topics}


