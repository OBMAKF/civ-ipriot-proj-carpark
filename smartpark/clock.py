# Student:          Nathan Bransby
# Student Number:   V141198

from datetime import datetime
from time import sleep
from broker import Broker


class Clock(Broker):
    """
    Publishes the current date and time every second.

    :param location:    The location that the car park is located. (used to identify the config file)
    :type location:     str
    """
    def __init__(self, location: str) -> None:
        super(Clock, self).__init__(
            config_file=f"{location}.toml",
            publishers=['time', 'date'])

        self.client.connect(
            self.config['broker_host'],
            self.config['broker_port'])

        self.mainloop()
    
    def mainloop(self):
        """Publishes the current date and time every second."""
        while True:
            message = [
                datetime.now().strftime('%H:%M:%S'),
                datetime.now().strftime('%d/%m/%y')]

            for i, topic in enumerate(self.publishers):
                self.client.publish(f"{self.config['location']}/{topic}", message[i])

            sleep(1)
    
    def on_message(self, client, userdata, message):
        pass


if __name__ == '__main__':
    Clock('test')
