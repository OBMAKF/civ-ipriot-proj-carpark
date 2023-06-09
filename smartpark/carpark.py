from broker import Broker
from clock import Clock


class CarPark(Broker):
    def __init__(self, location: str) -> None:
        super(CarPark, self).__init__(
            config_file=f"{location}.toml",
            subscriptions=['entry', 'exit'],
            publishers=['update_bays'])
        self.bays_available = self.config['total_spaces']
        self.client.connect(self.config['broker_host'], self.config['broker_port'])
        for topic in self.subscriptions:
            self.client.subscribe(f"{self.config['location']}/{topic}")
        self.client.loop_forever()
    
    def on_message(self, client, userdata, message):
        print(f"{message.payload.decode()}")
        if self.subscriptions is not None and \
                str(message.topic).startswith(f"{self.config['location']}"):
            for topic in self.subscriptions:
                if str(message.topic).endswith(topic):
                    match topic:
                        case 'entry':
                            self.on_entry()
                            break
                        
                        case 'exit':
                            self.on_exit()
                            break
                    return
    
    def on_entry(self):
        if self.bays_available > 0:
            self.bays_available -= 1
        self.publish()

    def on_exit(self):
        if self.bays_available < self.config['total_spaces']:
            self.bays_available += 1
        self.publish()
    
    def publish(self):
        for topic in self.publishers:
            self.client.publish(f"{self.config['location']}/{topic}", self.bays_available)
            print(topic)


if __name__ == '__main__':
    CarPark('test')
