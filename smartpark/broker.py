import paho.mqtt.client as mqtt
from config_parser import ConfigManager
from tomli import load
from abc import ABC, abstractmethod


class Broker(ABC):
    def __init__(
            self, config_file,
            subscriptions: list[str] = None,
            publishers: list[str] = None) -> None:
        self.config = dict()
        self.subscriptions = subscriptions
        self.publishers = publishers
        with ConfigManager(config_file) as file:
            config = load(file)
            self.config = config['config']
        
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
    
    @abstractmethod
    def on_message(self, client, userdata, message):
        pass
