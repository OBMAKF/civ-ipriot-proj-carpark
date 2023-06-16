from config_parser import ConfigManager
from tomli import load
import paho.mqtt.client as mqtt
import tkinter as tk


class TkDisplay(tk.Tk):
    subscriptions = ['update_bays', 'date', 'time', 'temperature']

    """
    Tkinter User Interface / Display unit. Connects to a car park via MQTT broker.
    
    Displays:
        - Current Date & Time.
        - Current Local Temperature (via API request).
        - The number of available car bays.
        - The location where the car park is located.
        
    :param location:   The location where the car park is location (used for finding config file).
    :type location:    str
    :param delay:      The length of the delay between each loop (in milliseconds)
    :type delay:       int  
    """
    def __init__(self, location, delay: int = 100, debug: bool = True) -> None:
        super(TkDisplay, self).__init__()
        self.debug = debug
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

        # Variables to store current readings
        self.current_date = tk.StringVar()
        self.current_time = tk.StringVar()
        self.current_temperature = tk.StringVar(value=f"18.0℃")
        self.current_bays = tk.StringVar(value=f"{self.config['total_spaces']}\nBays\n  Available  ")

        # Create labels to display current information
        self.bays = tk.Label(
            self, textvariable=self.current_bays,
            font=('Arial Bold', 40),
            foreground='red',
            background='black'
            )

        self.time = tk.Label(
            self, textvariable=self.current_time,
            font=('Arial', 18),
            foreground='white',
            background='black'
            )

        self.date = tk.Label(
            self, textvariable=self.current_date,
            font=('Arial', 18),
            foreground='white',
            background='black'
            )

        self.temperature = tk.Label(
            self, textvariable=self.current_temperature,
            font=('Arial', 18),
            foreground='white',
            background='black'
            )

        # Create buttons to allow the user to print a parking ticket / exit car park
        self.enter_button = tk.Button(self, text="Enter", command=self.on_entry)
        self.exit_button = tk.Button(self, text="Exit", command=self.on_exit)

        self.date.grid(column=0, row=1, sticky='W')
        self.temperature.grid(column=1, row=1)
        self.time.grid(column=2, row=1, sticky='E')
        self.bays.grid(column=0, columnspan=3, row=2)
        self.enter_button.grid(column=0, row=3, columnspan=2)
        self.exit_button.grid(column=1, row=3, columnspan=2)


        self.after(delay, lambda: self.get_update(delay))

        self.mainloop()
    
    def get_update(self, delay: int) -> None:
        """
        Updates the Display / listen to the network for subscriptions.

        Once called this function will be called periodically until manually terminated.

        :param delay:      The length of the delay between each loop (in milliseconds)
        :type delay:       int
        """
        self.client.loop()
        self.client.loop_read()
        self.after(delay, lambda: self.get_update(delay))
    
    def on_exit(self) -> None:
        """Event for simulating a car entering the car park."""
        self.client.publish(f"{self.config['location']}/exit")
    
    def on_entry(self) -> None:
        """Event for simulating a car exiting the car park."""
        self.client.publish(f"{self.config['location']}/entry")
    
    def on_message(self, client, userdata, message) -> None:

        print(f"{message.payload.decode()}") if self.debug else None

        if self.subscriptions is None:
            return

        targets = [self.current_bays, self.current_date, self.current_time, self.current_temperature]

        for topic in self.subscriptions:
            message_topic = ...
            content = ...
            target_index = ...
            result = ...

            if not message.topic.endswith(topic):
                continue

            match topic:
                case 'update_bays':
                    content = "\nBays\n  Available  "
                    target_index = 0

                case 'date':
                    target_index = 1

                case 'time':
                    target_index = 2

                case 'temperature':
                    target_index = 3

            content = f"{message.payload.decode('utf-8')}" if content is None else \
                f"{message.payload.decode('utf-8')}{content}"

            targets[target_index].set(content.replace('Ellipsis', ''))


if __name__ == '__main__':
    TkDisplay('test')
