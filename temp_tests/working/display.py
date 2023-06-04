from datetime import datetime
import tkinter as tk
import paho.mqtt.client as mqtt
from config_manager import ConfigManager
import threading
from tomli import load

sensor = None
previous_minute = 'N/A'


class TkDisplay(tk.Tk):

    HOST = 'localhost'
    PORT = 1883
    TOPIC = 'test'
    TOTAL_SPACES = 0

    def __init__(self, config_file, carpark) -> None:
        super(TkDisplay, self).__init__()
        self.carpark = carpark

        # open the confile file and assign variables.
        with ConfigManager(config_file) as configuration:
            config = load(configuration)['config']
            self.TOPIC = config['location']
            self.PORT = config['broker_port']
            self.HOST = config['broker_host']
            self.TOTAL_SPACES = config['total_spaces']

        self.title(self.TOPIC)

        global sensor, previous_minute
        sensor = tk.StringVar()
        previous_minute = tk.StringVar()
        self.current_time = tk.StringVar()
        self.current_date = tk.StringVar()
        self.last_temp = 'N/A'

        self.time_display = tk.Label(
            self, font=('Arial Bold', 24),
            background='#101010', foreground='#ffffff',
            justify='left', textvariable=self.current_time)

        self.date_display = tk.Label(
            self, font=('Arial Bold', 24),
            background='#101010', foreground='#ffffff',
            justify='left', textvariable=self.current_date)

        self.sensor_display = tk.Label(
            self, font=('Arial Bold', 24),
            background='#101010', foreground='#ffffff',
            justify='left')

        self.take_bay_button = tk.Button(
            self, command=self.carpark.assign_car,
            text="Purchase A Ticket")

        self.pay_fee_button = tk.Button(
            self, command=self.carpark.pay_fee,
            text="Pay Fee")

        self.time_display.grid(column=0, row=0)
        self.date_display.grid(column=0, row=1)
        self.sensor_display.grid(column=0, row=2)
        self.take_bay_button.grid(column=0, row=3, columnspan=2)
        self.pay_fee_button.grid(column=0, row=4, columnspan=2)

        self.client = mqtt.Client()
        self.connect()

    def connect(self):
        self.client.connect(self.HOST, self.PORT)
        self.client.on_message = self.on_message
        self.client.subscribe(self.TOPIC)
        self.get_update()
        self.mainloop()

    def get_update(self, delay: int = 100):
        self.current_time.set(datetime.now().strftime('%H:%M:%S'))
        self.current_date.set(datetime.now().strftime('%d-%m-%y'))

        last = previous_minute.get()

        if (last == '29' and datetime.now().strftime('%M') == '30')or \
                (last == '59' and datetime.now().strftime('%M') == '00'):
            self.carpark.publish()
        previous_minute.set("%M")


        if sensor.get().endswith(str(self.TOTAL_SPACES)):
            if self.pay_fee_button['state'] == 'normal':
                self.pay_fee_button.configure(state='disabled')
        elif self.pay_fee_button['state'] == 'disabled':
            self.pay_fee_button.configure(state='normal')

        self.client.loop()
        self.client.loop_read()
        self.sensor_display.configure(text=sensor.get())
        self.after(100, self.get_update)

    @staticmethod
    def on_message(client, userdata, message) -> None:
        if sensor is not None:
            sensor.set(f"{message.payload.decode()}")

    def mainloop(self, n: int = 0) -> None:
        super(TkDisplay, self).mainloop(n)

