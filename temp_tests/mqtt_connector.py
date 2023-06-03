import paho.mqtt.client as mqtt


class MQTTSubscriber:
    def __init__(self, target, config: dict):
        self.target = target
        self.LOCATION = config['location']
        self.HOST = config['broker_host']
        self.PORT = config['broker_port']
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.connect()

    def connect(self):
        self.client.connect(self.HOST, self.PORT)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def on_message(self, client, userdata, message):
        self.target.update_label(f"{message.payload.decode()}")
