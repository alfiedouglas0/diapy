import sys
import argparse
import configparser
from .config import Config

from .app.app import App

APP_NAME = "diapy"


def read_args():
    parser = argparse.ArgumentParser(APP_NAME)
    return parser.parse_args()


def main():
    args = read_args()

    app = App()
    app.run()


if __name__ == '__main__':
    main()
