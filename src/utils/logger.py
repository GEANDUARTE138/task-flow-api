"""
This module provides a custom logging handler using Loguru, with methods to log messages at various levels.

Classes:
    - Logger: A wrapper class to handle logging with different log levels.
    - LogHandler: A singleton class to configure and manage the root logger.
"""

import json
import os
import sys
from loguru import logger
from shared.constants import SERVICE_NAME
from utils.singleton import Singleton



logger.disable("uvicorn.error")
logger.disable("uvicorn.access")
logger.disable("uvicorn.asgi")
logger.disable("asyncio")
logger.disable("urllib3.connectionpool")
logger.disable("chardet.charsetprober")


class Logger:
    """
    A logger class that wraps the Loguru logger to provide logging at various levels (debug, info, warning, error, fatal).
    
    Args:
        class_name (str): The name of the class using this logger, used for logging context.
    """

    def __init__(self, class_name):
        self.logger = LogHandler().get_logger(class_name)

    def debug(self, msg, message_json={}):
        """
        Log a debug message.

        Args:
            msg (str): The log message.
            message_json (dict): Additional JSON data to include in the log (default is an empty dictionary).
        """
        log_json = self.__prepare_log(msg, message_json)
        self.logger.debug(log_json)

    def info(self, msg, message_json={}):
        """
        Log an info message.

        Args:
            msg (str): The log message.
            message_json (dict): Additional JSON data to include in the log (default is an empty dictionary).
        """
        log_json = self.__prepare_log(msg, message_json)
        self.logger.info(log_json)

    def warning(self, msg, message_json={}):
        """
        Log a warning message.

        Args:
            msg (str): The log message.
            message_json (dict): Additional JSON data to include in the log (default is an empty dictionary).
        """
        log_json = self.__prepare_log(msg, message_json)
        self.logger.warning(log_json)

    def error(self, msg, message_json={}):
        """
        Log an error message.

        Args:
            msg (str): The log message.
            message_json (dict): Additional JSON data to include in the log (default is an empty dictionary).
        """
        log_json = self.__prepare_log(msg, message_json)
        self.logger.error(log_json)

    def fatal(self, msg, message_json={}):
        """
        Log a fatal message.

        Args:
            msg (str): The log message.
            message_json (dict): Additional JSON data to include in the log (default is an empty dictionary).
        """
        log_json = self.__prepare_log(msg, message_json)
        self.logger.critical(log_json)

    def __prepare_log(self, msg, message_json):
        """
        Prepare the log message and related metadata as a JSON string.

        Args:
            msg (str): The main log message.
            message_json (dict): Additional JSON data to include in the log.

        Returns:
            str: A JSON-formatted string containing the log message and metadata.
        """
        log_json = dict()
        log_json["message"] = msg
        log_json["message_json"] = message_json
        log_json["pid"] = str(os.getpid())
        return json.dumps(log_json)


class LogHandler(metaclass=Singleton):
    """
    A singleton class that configures and manages the root logger for the application using Loguru.
    """

    def __init__(self) -> None:
        self.__setup_root_logger()

    def get_logger(self, class_name):
        """
        Get a logger instance bound to a specific class name.

        Args:
            class_name (str): The name of the class using the logger.

        Returns:
            logger: A Loguru logger instance.
        """
        logger_name = f"{SERVICE_NAME}.{class_name}"
        return logger.bind(name=logger_name)

    def __setup_root_logger(self):
        """
        Set up the root logger with a specific log level and output configuration.
        """
        log_level = "DEBUG"
        logger.remove()
        logger.add(sys.stdout, level=log_level)
