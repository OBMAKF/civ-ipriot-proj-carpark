import paho.mqtt.client as mqtt
from datetime import datetime
from tomli import load
from abc import ABC, abstractmethod
from config_manager import ConfiguationManager


class MQTT(ABC):
    TOPIC = None
    BROKER_HOST = None
    BROKER_PORT = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def on_message(self, client, userdata, message):
        pass


class MQTTSubscriber(MQTT):
    def __init__(self, config_file, topic, **kwargs):
        self.TOPIC = topic
        with ConfiguationManager(config_file) as file:
            self.BROKER_HOST = load(file)['config']['broker_host']
            self.BROKER_PORT = load(file)['config']['broker_port']
            self.subscriptions = file[topic]
            self.subscriptions[kwargs] = file[kwargs]

        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.BROKER_HOST, self.BROKER_PORT)
        self.client.on_message = self.on_message
        self.get_update()

    def on_message(self, client, userdata, message) -> dict:
        results = {}
        results['time'] = datetime.now().strftime('%H:%M:%S')
        results['date'] = datetime.now().strftime('%d/%m/%y')
        for topic in self.subscriptions:
            if message.topic == topic:
                results[topic] = f"{message.payload.decode()}"
            continue
        return results

    def get_update(self):
        pass


class MQTTPublisher(MQTT):
    def __init__(self, config, topic):
        pass
