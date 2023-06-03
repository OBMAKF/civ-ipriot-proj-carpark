from mqtt_connector import MQTTSubscriber
import tkinter as tk
import tomli


class ConfigManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def __enter__(self):
        self.file = open(self.file_name, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


class Window(tk.Tk):
    def __init__(self, config_file):
        super(Window, self).__init__()

        self.label = tk.Label(self).pack()

        self.config = {}

        with ConfigManager(config_file) as config:
            self.config = tomli.load(config)

        self.connection = MQTTSubscriber(self, self.config['config'])
        self.subscribe()
        self.check_messages()

    def check_messages(self):
        self.connection.client.loop(0)
        self.after(1000, self.check_messages)
        self.mainloop()

    def subscribe(self):
        self.connection.subscribe(self.config['config']['location'])

    def update_label(self, message) -> None:
        self.label.configure(text=message)



if __name__ == '__main__':
    window = Window('joondalup_city_square.toml')
    print(window.config)
