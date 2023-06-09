from typing import BinaryIO


class ConfigManager:
    def __init__(self, config_file) -> None:
        self.filename = config_file
    
    def __enter__(self) -> BinaryIO:
        try:
            self.file = open(self.filename, 'rb')
            return self.file
        except FileNotFoundError as error:
            raise error
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.file.close()
