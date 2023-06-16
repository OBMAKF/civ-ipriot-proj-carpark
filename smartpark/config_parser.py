# Student:          Nathan Bransby
# Student Number:   V141198

from typing import BinaryIO


class ConfigManager:
    """
    Manager for opening .TOML config files.

    :param config_file:  Filename of the TOML config file.
    :type config_file:   str

    :returns: The open config file converted to Binary.IO.
    """
    def __init__(self, config_file) -> None:
        self.filename = config_file
    
    def __enter__(self) -> BinaryIO:
        """
        Open the file and return in Binary.IO format

        :returns: self.file
        :rtype:   BinaryIO
        """
        try:
            self.file = open(self.filename, 'rb')
            return self.file

        except FileNotFoundError as error:
            raise error
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Close binary file on exit."""
        self.file.close()
