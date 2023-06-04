class ConfigManager:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()