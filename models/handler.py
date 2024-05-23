import os
import threading
from abc import abstractmethod, ABC
from enum import Enum


class LevelEnum(Enum):
    """
    Level Enum
    """
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5


class LoggerTypeEnum(Enum):
    """
    Logger Type
    """
    SYNC = 1
    ASYNC = 2


class Handler(ABC):
    """
    priyakumari.m@flipkart.com
    ts_format:dd-mm-yyyy-hh-mm-ss
    log_level:INFO
    logger_type:ASYNC
    buffer_size:25
    sink_type:STDOUT

    msg_format: 27-06-2019-09-30-00 [INFO] This is a sample log message.
    """

    def __init__(self, level: LevelEnum, logger_type: LoggerTypeEnum, time_format: str = "%D-%H:%M:%S", **kwargs):
        """

        :param level: LevelEnum
        :param logger_type: LoggerTypeEnum
        :param time_format: Has to support python datetime format
        :param kwargs:
        """
        self.__level = level
        self.__time_format = time_format
        self.__logger_type = logger_type
        self.__buffer_size = kwargs.get('buffer_size', 25)
        self.__buffer_count = 0
        self.__lock = threading.Lock()
        self.__condition = threading.Condition()
        self.__buffer_lock = threading.Lock()

    def get_time(self) -> str:
        from datetime import datetime
        return datetime.now().strftime(self.__time_format)

    @abstractmethod
    def _log(self, msg: str, level: LevelEnum):
        raise NotImplementedError("This method is not implemented")

    def __can_log(self, level: LevelEnum) -> bool:
        print(self.__level.name, level.name, "===", self.__level.value <= level.value)
        return self.__level.value <= level.value

    def __async_log(self, func):
        while self.__buffer_lock.locked():
            pass
        with self.__lock:
            self.__buffer_count += 1
        if self.__buffer_count >= self.__buffer_size:
            self.__buffer_lock.acquire()

        def callback():
            with self.__lock:
                self.__buffer_count -= 1
            if self.__buffer_count < self.__buffer_size and self.__buffer_lock.locked():
                self.__buffer_lock.release()

        thread = threading.Thread(target=func, args=([callback]))
        thread.start()

    def __sync_log(self, func):
        func()

    def log(self, msg: str, level: LevelEnum):
        if self.__can_log(level):
            def func(callback=None):
                self._log(msg, level)
                if callback:
                    callback()

            if self.__logger_type == LoggerTypeEnum.SYNC:
                self.__sync_log(func)
            else:
                self.__async_log(func)

    @property
    def level(self):
        return self.__level


class DebugHandler(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__print_lock = threading.Lock()

    def _log(self, msg: str, level: LevelEnum):
        with self.__print_lock:
            print(f"{self.get_time()} [{level.name}] {msg}")


class FileHandler(Handler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__file_path = kwargs.get('file_path')
        if not self.__file_path:
            raise Exception("File path should be provided")
        # if not self.__check_file_exists():
        #     raise Exception("Log file does't exist")

    def __check_file_exists(self) -> bool:
        return os.path.exists(self.__file_path)

    def _log(self, msg: str, level: LevelEnum):
        with open(self.__file_path, 'a') as f:
            f.write(f"{self.get_time()} [{level.name}] {msg}\n")
