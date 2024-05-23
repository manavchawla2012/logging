from typing import List

from models.handler import Handler, DebugHandler, LevelEnum, LoggerTypeEnum, FileHandler

"""
You can register handlers here which will be utilised by the logging service
"""

HANDLERS: List[Handler] = [
    DebugHandler(level=LevelEnum.ERROR, logger_type=LoggerTypeEnum.ASYNC, buffer_size=10),
    FileHandler(level=LevelEnum.ERROR, logger_type=LoggerTypeEnum.SYNC, file_path="./logs/project.log"),
]
