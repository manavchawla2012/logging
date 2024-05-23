from typing import List

from config import HANDLERS
from models.handler import LevelEnum, Handler


class LoggingService:
    """
    This is singelton class to handle logging.
    """
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, handlers: List[Handler]):
        """
        :param handlers: All the available handlers
        """
        self.__handlers: List[Handler] = handlers

    def log(self, message: str, level: LevelEnum):
        """
        Logs message to all available handlers
        :param message: string to be logged
        :param level: level of message
        :return: None
        """
        for handler in self.__handlers:
            handler.log(message, level)


# initializing logging object.
logger = LoggingService(HANDLERS)
