# Student:          Nathan Bransby
# Student Number:   V141198

from carpark import CarPark
from clock import Clock
from temperature_sensor import TemperatureSensor
from display import TkDisplay

import threading


def initialize_components(location: str) -> None:
    """Create and run a new threaded object for each major functional
    component required for running a smart car park system.

    (Required for running multiple events loops together whilst
    displaying a Tkinter GUI.)

    :param location:    Takes a specified location, to determine the config file.
    :type location:     str
    """
    threads = [
        threading.Thread(target=lambda: CarPark(location)),
        threading.Thread(target=lambda: Clock(location)),
        threading.Thread(target=lambda: TemperatureSensor(location)),
        threading.Thread(target=lambda: TkDisplay(location))]

    for thread in threads:
        thread.start()

if __name__ == '__main__':
    initialize_components('moondalup')
