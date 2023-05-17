from sense_hat import SenseHat


class Sensor:
    def __init__(self) -> None:
        """Initialize the Sensor object with a SenseHat instance."""
        self.sense_hat = SenseHat

    def read_temperature(self) -> float:
        """Read the temperature from the SenseHat sensor."""
        pass
