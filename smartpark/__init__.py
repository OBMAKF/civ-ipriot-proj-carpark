from carpark import CarPark
from clock import Clock
from temperature_sensor import TemperatureSensor
from display import TkDisplay

import threading


if __name__ == '__main__':
    threads = [
        threading.Thread(target=lambda: CarPark('test')),
        threading.Thread(target=lambda: Clock('test')),
        threading.Thread(target=lambda: TemperatureSensor('test')),
        threading.Thread(target=lambda: TkDisplay('test'))]
    for thread in threads:
        thread.start()
