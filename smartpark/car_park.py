import paho.mqtt.client as mqtt


class ParkingLot:
    def __init__(self, location: str, total_spaces: int,  # todo -- __init__(self, config) <-- read the config file.
                 available_spaces: int, mqtt_client=None) -> None:
        """Initialize the ParkingLot object with the given configuration."""
        self.location = location
        self.total_spaces = total_spaces
        self.available_spaces = available_spaces
        self.mqtt_client = mqtt_client  # The MQTT client to send and receive messages.

    def enter(self) -> None:
        """Register a car entering the parking lot."""
        if 1 <= self.available_spaces <= self.total_spaces:
            self.available_spaces += 1
            return
        # todo - display message????
        pass

    def exit(self) -> None:
        """Register a car leaving the parking lot"""
        self.available_spaces -= 1
        pass

    def publish_update(self) -> None:
        """Publish an update containing available_spaces, temperature and time."""
        pass
