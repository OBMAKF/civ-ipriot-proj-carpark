from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = 'localhost'
PORT = 1883

TOPIC = 'ParkingLot/incoming'


def on_message(client, userdata, message):
    """Get MQTT message"""
    print(f"Received {message.payload.decode()}")


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.subscribe(TOPIC)
    client.loop_forever()
