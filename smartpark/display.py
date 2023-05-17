from sense_hat import SenseHat


class Display:

    def __init__(self) -> None:
        """Initialize the Display object with a SenseHAT instance."""
        self.sense_hat = SenseHat()

    def show_message(self, message: str) -> None:
        """Display a message on the LED display."""
        self.sense_hat.show_message(message)  # todo
        pass
