import sys
from abc import ABC, abstractmethod


class Logger(ABC):

    @abstractmethod
    def info(self, message: str):
        pass

    def error(self, message: str):
        pass


class StandardOutputLogger(Logger):

    def info(self, message: str):
        print(message, file=sys.stdout)

    def error(self, message: str):
        print(message, file=sys.stderr)
