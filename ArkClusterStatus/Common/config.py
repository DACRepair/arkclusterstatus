import os
from configparser import ConfigParser


class Config:
    def __init__(self, path: str = None):
        if path is None:
            path = os.path.normpath(os.getcwd() + "/config.ini")
        else:
            path = os.path.normpath(path)
        self.config = ConfigParser()
        if os.path.isfile(path):
            self.config.read(path)

    def get(self, section: str, option: str, default: str = None, wrap=None):
        section = section.lower()
        option = option.lower()
        env = section.upper() + "__" + option.upper()

        value = os.getenv(env, self.config.get(section, option, fallback=default))

        if wrap is not None and callable(wrap):
            value = wrap(value)
        return value
