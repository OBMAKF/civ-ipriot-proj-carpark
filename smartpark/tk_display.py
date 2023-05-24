from datetime import datetime
import tkinter as tk
import paho.mqtt.client as mqtt
import threading

sensor = None


class TkDisplay(tk.Tk):

    HOST = 'localhost'
    PORT = 1883
    TOPIC = 'test'

    def __init__(self) -> None:
        super(TkDisplay, self).__init__()
        global sensor
        sensor = tk.StringVar()

        self.time_display = tk.Label(
            self, font=('Arial Bold', 24), background='#101010', foreground='#ffffff')
        self.sensor_display = tk.Label(
            self, font=('Arial Bold', 24), background='#101010', foreground='#ffffff')
        self.time_display.grid(column=0, row=0, sticky='W')
        self.sensor_display.grid(column=0, row=1)

        self.client = mqtt.Client()
        self.client.connect(self.HOST, self.PORT)
        self.client.on_message = self.on_message
        self.client.subscribe(self.TOPIC)
        self.after(10, self.get_update())
        self.mainloop()

    def get_update(self, delay: int = 100):
        self.time_display.configure(text=str(datetime.now()))
        self.client.loop()
        self.client.loop_read()
        self.sensor_display.configure(text=sensor.get())
        self.after(1000, self.get_update)

    @staticmethod
    def on_message(client, userdata, message) -> None:
        if sensor is not None:
            sensor.set(f"{datetime.now()} - {message.payload.decode()}")

    def mainloop(self, n: int = 0) -> None:
        super(TkDisplay, self).mainloop(n)








"""


class SensorLabel(tk.Label):
    def __init__(self, parent: tk.Misc, sensor_id: str) -> None:
        super(SensorLabel, self).__init__(parent)

        self.id = sensor_id
        self.in_display = False

    def display(self) -> None:
        if not self.in_display:
            self.pack()
            self.in_display = True
        self.configure(text=self.master.fetch_info(self.id))


class Display(tk.Tk):
    def __init__(self, broker) -> None:
        super(Display, self).__init__()
        self.layout = {}

        self.broker = broker

    def fetch_info(self, sensor_id):
        # return broker message
        pass

    def mainloop(self, n: int = 0) -> None:
        super(Display, self).mainloop(n)


class SensorDisplay(tk.Tk):
    def __init__(self) -> None:
        super(SensorDisplay, self).__init__()
        self.title("Car Detector ULTRA")

        self.is_running = False

        # Represents the sensor detecting an incoming vehicle
        self.incoming_vehicle_button = tk.Button(
            self, text="Vehicle In",
            command=lambda: self.register_incoming_vehicle())

        # Represents the sensor detecting an outgoing vehicle
        self.outgoing_vehicle_button = tk.Button(
            self, text="Vehicle Out",
            command=lambda: self.register_outgoing_vehicle())

        # Set up the display
        self.incoming_vehicle_button.grid(column=0, row=0)
        self.outgoing_vehicle_button.grid(column=1, row=0)

        self.mainloop(  )

    def run(self, delay: int = 100) -> None:
        if self.is_running:
            return
        self.is_running = True
        self.after(delay, self.update_info(delay))

    def update_info(self, interval: int):
        self.mainloop(interval)

    def register_incoming_vehicle(self):
        # TODO: implement this method to publish the detection via MQTT
        print("Car goes in")
        pass

    def register_outgoing_vehicle(self):
        # TODO: implement this method to publish the detection via MQTT
        print("Car goes out")
        pass

    def mainloop(self, n: int = 0) -> None:
        super(SensorDisplay, self).mainloop(n)

"""
if __name__ == '__main__':
    TkDisplay()
