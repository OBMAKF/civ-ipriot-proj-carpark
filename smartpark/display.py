from config_parser import ConfigManager
from tomli import load
import paho.mqtt.client as mqtt
import tkinter as tk


class TkDisplay(tk.Tk):
    subscriptions = ['update_bays', 'date', 'time', 'temperature']
    
    def __init__(self, location) -> None:
        super(TkDisplay, self).__init__()
        self.configure(background='black')

        with ConfigManager(f"{location}.toml") as file:
            config = load(file)
            self.config = config['config']
        self.title(self.config['location'])
        
        self.client = mqtt.Client()
        self.client.connect(self.config['broker_host'], self.config['broker_port'])
        self.client.on_message = self.on_message
        
        # Subscribe to topics
        for topic in self.subscriptions:
            self.client.subscribe(f"{self.config['location']}/{topic}")
        
        self.current_date = tk.StringVar()
        self.current_time = tk.StringVar()
        self.current_temperature = tk.StringVar(value=f"18.0℃")
        self.current_bays = tk.StringVar(
            value=f"{self.config['total_spaces']}\nBays\n  Available  ")
        
        self.bays = tk.Label(
            self, textvariable=self.current_bays, font=('Arial Bold', 40),
            foreground='red', background='black')
        self.time = tk.Label(
            self, textvariable=self.current_time, font=('Arial', 18),
            foreground='white', background='black')
        self.date = tk.Label(
            self, textvariable=self.current_date, font=('Arial', 18),
            foreground='white', background='black')
        self.temperature = tk.Label(
            self, textvariable=self.current_temperature, font=('Arial', 18),
            foreground='white', background='black')
        self.enter_button = tk.Button(self, text="Enter", command=self.entry)
        self.exit_button = tk.Button(self, text="Exit", command=self.exit)

        self.date.grid(column=0, row=1, sticky='W')
        self.temperature.grid(column=1, row=1)
        self.time.grid(column=2, row=1, sticky='E')
        self.bays.grid(column=0, columnspan=3, row=2)
        self.enter_button.grid(column=0, row=3, columnspan=2)
        self.exit_button.grid(column=1, row=3, columnspan=2)
        
        self.after(100, self.get_update)
        self.mainloop()
    
    def get_update(self):
        self.client.loop()
        self.client.loop_read()
        self.after(100, self.get_update)
    
    def exit(self):
        self.client.publish(f"{self.config['location']}/exit")
    
    def entry(self):
        self.client.publish(f"{self.config['location']}/entry")
    
    def on_message(self, client, userdata, message):
        print(f"{message.payload.decode()}")
        if self.subscriptions is not None and \
                str(message.topic).startswith(f"{self.config['location']}"):
            for topic in self.subscriptions:
                if str(message.topic).endswith(topic):
                    match topic:
                        case 'update_bays':
                            self.current_bays.set(
                                f"{message.payload.decode('utf-8')}\nBays\n  Available  ")
                            break
                        
                        case 'date':
                            self.current_date.set(f"{message.payload.decode('utf-8')}")
                            break
                        
                        case 'time':
                            self.current_time.set(f"{message.payload.decode('utf-8')}")
                            break
                        
                        case 'temperature':
                            self.current_temperature.set(f"{message.payload.decode('utf-8')}")
                            break
                        
                    return


if __name__ == '__main__':
    TkDisplay('test')
