from broker import Broker


class CarPark(Broker):
    """ Represents a physical car park.
    Manages the current count of available car bays and handles any incoming / outgoing vehicles.

    :param location:    The location of the car park (used for reading the correct config file).
    :type location:     str
    """
    def __init__(self, location: str, debug: bool = True) -> None:

        super(CarPark, self).__init__(
            config_file=f"{location}.toml",
            subscriptions=['entry', 'exit'],
            publishers=['update_bays']
        )

        self.debug = debug

        self.bays_available = self.config['total_spaces']
        self.client.connect(self.config['broker_host'], self.config['broker_port'])

        # Subscribe to subscriptions
        for topic in self.subscriptions:
            self.client.subscribe(f"{self.config['location']}/{topic}")

        self.client.loop_forever()
    
    def on_message(self, client, userdata, message) -> None:

        print(f"{message.payload.decode()}") if self.debug is True else None

        if not self.subscriptions:
            return

        message_topic = f"{message.topic}"

        for topic in self.subscriptions:

            event = ...

            # Ensure the topic is in subscriptions
            if not message_topic.endswith(topic):
                continue

            match topic:

                case 'entry':
                    event = self.on_entry

                case 'exit':
                    event = self.on_exit

            return event() if not None else None

    def on_entry(self) -> None:
        """
        Handles an incoming vehicle when a vehicle enters the car park.

        Adjust the number of available car bays if any bays are available.
        When triggered publish the total bay availability across the network.
        """

        if self.bays_available > 0:
            self.bays_available -= 1
        self.publish()

    def on_exit(self) -> None:
        """
        Handles an outgoing vehicles when a vehicle enters the car park.

        Adjust the number of available car bays when a vehicle leaves.
        When triggered publish the total bay availability across the network.
        """
        if self.bays_available < self.config['total_spaces']:
            self.bays_available += 1
        self.publish()
    
    def publish(self):
        """
        Method for publishing the current number of available bays.

        [ Topic =>  "{location}/update_bays" ]
        """
        for topic in self.publishers:
            print(topic) if self.debug else None
            self.client.publish(f"{self.config['location']}/{topic}", self.bays_available)


if __name__ == '__main__':
    CarPark('test')
