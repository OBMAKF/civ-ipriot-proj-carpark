import paho.mqtt.client as mqtt
from config_parser import ConfigManager
import tomli
from abc import ABC, abstractmethod


class Broker(ABC):
    """
    Base class for creating an instance of an MQTT Broker.

    Uses:
        - Configure a class from a `.TOML` file.
        - Manage subscriptions and publishing topics.
        - Create an instance of a `paho-mqtt client` and bind methods.
        - Indicate the requirement for a `on_message` function when inherited.

    :param config_file:     The filename of the configuration file ( .toml )
    :type config_file:      str
    :param subscriptions:   A list containing all relevant subscription topics.
    :type subscriptions:    list[str] | None
    :param publishers:      A list containing all relevant topics to publish to.
    :type publishers:       list[str] | None
    """
    def __init__(self, config_file, subscriptions: list[str] = None,
                 publishers: list[str] = None) -> None:

        self.config = dict()
        self.subscriptions = subscriptions
        self.publishers = publishers

        # Read the config file and save configuration
        with ConfigManager(config_file) as file:
            config = tomli.load(file)
            self.config = config['config']
        
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
    
    @abstractmethod
    def on_message(self, client, userdata, message) -> None:
        """Abstract Method for manging events whenever a
         subscribed topic is sent over the network.

         This method must be implemented by all classes that
         inherit a Broker."""
        pass
