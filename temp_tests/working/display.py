from datetime import datetime
import tkinter as tk
import paho.mqtt.client as mqtt
from config_manager import ConfigManager
import threading
from tomli import load

sensor = None
last_reading = 'N/A'


class TkDisplay(tk.Tk):

    HOST = 'localhost'
    PORT = 1883
    TOPIC = 'test'

    def __init__(self, config_file, carpark) -> None:
        super(TkDisplay, self).__init__()
        with ConfigManager(config_file) as config:
            config = load(config)['config']
            self.TOPIC = config['location']
            self.PORT = config['broker_port']
            self.HOST = config['broker_host']
        self.carpark = carpark
        global sensor, last_reading
        sensor = tk.StringVar()
        last_reading = tk.StringVar()
        self.last_temp = 'N/A'
        self.time_display = tk.Label(
            self, font=('Arial Bold', 24), background='#101010', foreground='#ffffff',
            justify='left')
        self.sensor_display = tk.Label(
            self, font=('Arial Bold', 24), background='#101010', foreground='#ffffff',
            justify='left')
        self.take_bay_button = tk.Button(self, command=self.carpark.assign_car)
        self.time_display.grid(column=0, row=0, sticky='W')
        self.sensor_display.grid(column=0, row=1)
        self.take_bay_button.grid(column=0, row=2, columnspan=2)

        self.client = mqtt.Client()
        self.connect()

    def connect(self):
        self.client.connect(self.HOST, self.PORT)
        self.client.on_message = self.on_message
        self.client.subscribe(self.TOPIC)
        self.after(10, self.get_update())
        self.mainloop()

    def get_update(self, delay: int = 100):
        self.time_display.configure(text=f"{last_reading.get()}")
        self.client.loop()
        self.client.loop_read()
        self.sensor_display.configure(text=sensor.get())
        self.after(1000, self.get_update)

    @staticmethod
    def on_message(client, userdata, message) -> None:
        if sensor is not None:
            sensor.set(f"{message.payload.decode()}")
            last_reading.set(f"{message.payload.decode()}")

    def mainloop(self, n: int = 0) -> None:
        super(TkDisplay, self).mainloop(n)

