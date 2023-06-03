from mqtt_messenger import MQTT_Client
from carpark import Carpark
import tkinter as tk
import asyncio


class TkDisplay(tk.Tk):
    TOPICS = []

    def __init__(self, carpark: Carpark, topics: list[str]) -> None:
        super(TkDisplay, self).__init__()
        self.TOPICS = topics
        self.title(carpark.LOCATION)
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.carpark = carpark

        self.content = tk.Label(self)
        self.subscribe_button = tk.Button(self, text="subscribe", command=self.subscribe)
        self.disconnect_button = tk.Button(self, text="disconnect", command=self.disconnect)

        self.user_interface = [[]]

        self.connection = MQTT_Client(self, self.TOPICS)

    def activate(self, location: tuple[int, int]):
        pass # todo - update bay

    def check_messages(self):
        self.connection.client.loop(0)
        self.after(1000, self.check_messages)

    def subscribe(self):
        for topic in self.TOPICS:
            self.connection.subscribe(topic)
        self.subscribe_button.configure(state='disabled')
        self.disconnect_button.configure(state='normal')

    def disconnect(self):
        self.connection.disconnect()
        self.destroy()

    def update_label(self, message: str, topic: str):
        self.content.configure(text=message)
