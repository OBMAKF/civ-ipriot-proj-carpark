from mqtt_messenger import MQTT_Client
import tkinter as tk
import asyncio


class TkDisplay(tk.Tk):
    def __init__(self) -> None:
        super(TkDisplay, self).__init__()
        self.content = tk.Label
        self.broker = MQTT_Client(self)

    def set_display(self, content: str = None):
        self.content = content

    async def run(self, delay: int = 100):
        while await asyncio.sleep(delay, True):
            self.set_display = self.broker.ping()
            self.update()

