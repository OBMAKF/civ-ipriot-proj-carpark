from carpark import CarPark
from clock import Clock
from temperature_sensor import TemperatureSensor
from display import TkDisplay

import threading


if __name__ == '__main__':
    threads = [
        threading.Thread(target=lambda: CarPark('moondalup')),
        threading.Thread(target=lambda: Clock('moondalup')),
        threading.Thread(target=lambda: TemperatureSensor('moondalup')),
        threading.Thread(target=lambda: TkDisplay('moondalup'))]
    for thread in threads:
        thread.start()
