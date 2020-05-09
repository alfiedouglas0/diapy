import configparser
from os.path import dirname, join, abspath

from .utils import classproperty

ROOT_PATH = dirname(abspath(__file__))
CONFIG_NAME = "config.ini"


class Config:
    """ Static class as a wrapper around the config """
    _class_instance = None

    def __init__(self):
        self.load_config()

    @staticmethod
    def get_root_path() -> str:
        return ROOT_PATH

    @classproperty
    def singleton(cls):
        if cls._class_instance is None:
            cls._class_instance = Config()
        return cls._class_instance

    def load_config(self):
        self._config = configparser.ConfigParser()
        self._config.read(join(ROOT_PATH, CONFIG_NAME))

    def save_config(self):
        with open(join(ROOT_PATH, CONFIG_NAME), 'w') as configfile:
            self._config.write(configfile)

    @property
    def store_path(self) -> str:
        if(self._config["USER"]["StorePath"] == ""):
            return ROOT_PATH
        return self._config["USER"]["StorePath"]

    @store_path.setter
    def store_path(self, val: str):
        self._config["USER"]["StorePath"] = val

    @property
    def db_name(self) -> str:
        if self._config["USER"]["DBName"] == "":
            return self._config["DEFAULT"]["DBName"]
        return self._config["USER"]["DBName"]

    @db_name.setter
    def db_name(self, val: str):
        self._config["USER"]["DBName"] = val

    def get_db_path(self) -> str:
        return abspath(join(self.store_path, self.db_name))
