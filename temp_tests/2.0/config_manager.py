class ConfigurationManager:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    def __enter__(self) -> IO:
        self.file = open(self.filename, 'rb')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.file.close()