
class ConfigManager:
    def __init__(self, config) -> None:
        self.config = config

    def __new__(cls, *args, **kwargs):
        return ConfigManager(tuple(**kwargs))

    def __enter__(self):
        self.host = self.config['HOST']
        self.port = self.config['PORT']
        self.topic = self.config['TOPICS']

    def __exit__(self, exc_type, exc_val, exc_tb):
        return "{0}/{1}/{2}".format(self.host, self.port, self.topic)
