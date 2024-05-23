import threading

from models.handler import LevelEnum
from service.logging_service import logger
import random

if __name__ == '__main__':

    """
    Project Structure:
    
    1. Models
        a. Handler
    2. Logging Service -> For accessing the logging object
    
    
    
    """

    threads = []
    level_options = [level for level in LevelEnum]

    def logs_for_thread(count):
        for i, message in enumerate(list(range(count * 25, (count + 1) * 25))):
            logger.log(f"{str(message)}: for thread {count + 1}", random.choice(level_options))


    for i in range(4):
        thread = threading.Thread(target=logs_for_thread, args=([i]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
