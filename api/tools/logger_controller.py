import logging
from logging.handlers import TimedRotatingFileHandler
import sys


class Logger:

    def __init__(self, name: str):
        """Initialize the logger for file handler and STDOUT
        Args:
        -----
            name (str): name of the logger (comes after the level).
        """

        self.log = logging.getLogger(name)
        self.log.setLevel(logging.DEBUG)

        logFormatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s --- [%(name)-8s] : %(message)s")

        fileHandler = TimedRotatingFileHandler(
            f"./logs/{name}.log", when="midnight")
        fileHandler.setFormatter(logFormatter)
        fileHandler.suffix = "%Y_%m_%d"
        self.log.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        self.log.addHandler(consoleHandler)