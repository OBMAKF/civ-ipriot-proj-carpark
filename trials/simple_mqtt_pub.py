from datetime import datetime
import paho.mqtt.client as mqtt

BROKER = 'localhost'
PORT = 1883

TOPIC = 'ParkingLot/incoming'0


if __name__ == '__main__':
    client = mqtt.Client()

    client.connect(BROKER, PORT)
    client.publish(TOPIC, "test")