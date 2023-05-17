import paho.mqtt.client as mqtt

# todo!!!
broker_host = ""
broker_port = ""

# Create an MQTT client
client = mqtt.Client()

# Connect the client to the MQTT broker
client.connect(broker_host, broker_port)

# Subscribe to a topic to receive messages
client.subscribe("topic_name")


def on_message(client, userdata, message):
    pass


class Client(mqtt.Client):
    def __init__(self, broker_host, broker_port) -> None:
        super(Client, self).__init__()
        self.host = broker_host
        self.port = broker_port

    def connect(self, host, port=1883, keepalive=60, bind_address="", bind_port=0,
                clean_start=False, properties=None) -> None:
        super(Client, self).connect(self.host, self.port)

    def subscribe(self, topic, qos=0, options=None, properties=None) -> None:
        super(Client, self).subscribe(topic)




