import sys
from os.path import dirname, join
import argparse
import configparser

APP_NAME = "diapy"

CONFIG_PATH = "config.ini"
DB_PATH = None


def read_args():
    parser = argparse.ArgumentParser(APP_NAME)
    return parser.parse_args()


def read_config():
    config = configparser.ConfigParser()
    config.read(join(dirname(__file__), CONFIG_PATH))
    global DB_PATH
    DB_PATH = join(dirname(__file__), config["DEFAULT"]["StorePath"],
                   config["DEFAULT"]["StoreDB"])
    return config


def main():
    args = read_args()
    config = read_config()

    print(DB_PATH)


if __name__ == '__main__':
    main()
