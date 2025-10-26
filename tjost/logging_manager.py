"""Logging manager for configuring and handling log outputs"""

import logging
from importlib.metadata import metadata


logger = logging.getLogger(__name__)

logging.addLevelName(logging.CRITICAL, "Crit")
logging.addLevelName(logging.DEBUG, "Debug")
logging.addLevelName(logging.ERROR, "Error")
logging.addLevelName(logging.INFO, "Info")
logging.addLevelName(logging.WARNING, "Warn")


class LoggingManager:
    """Manages logging configuration"""

    __format: str = "[{levelname:<5}] {message} ({name}:{lineno})"
    __formatter: logging.Formatter = logging.Formatter(__format, style="{")
    __verbosity: dict = {
        0: logging.ERROR,
        1: logging.WARNING,
        2: logging.INFO,
    }

    def __init__(self, verbosity: int):
        """
        Initialize logging with the specified verbosity level.
        Automatically adds a stream handler for console output.

        The verbosity levels are mapped as follows:
        - 0: ERROR
        - 1: WARNING
        - 2: INFO
        - 3 or higher: DEBUG

        :param verbosity: Verbosity level
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(self.__verbosity.get(verbosity, logging.DEBUG))
        stream_handler.setFormatter(self.__formatter)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(stream_handler)
        logger.info("Logging initialized")
        logger.info(f"Stream handler with verbosity {verbosity} added to logging")

    def add_journal_handler(self, verbosity: int):
        """
        Add a systemd journal handler with the specified verbosity level.
        The verbosity parameter behaves the same way as in the constructor.

        :param verbosity: Verbosity level
        """
        try:
            from systemd.journal import JournalHandler
        except ImportError as e:
            logger.warning("Failed to import JournalHandler from systemd.journal")
            logger.warning("Systemd journal logging will not be available")
            logger.debug(f"ImportError details: {e}")
            return

        journal_handler = JournalHandler(SYSLOG_IDENTIFIER=metadata("tjost")["Name"])
        journal_handler.setLevel(self.__verbosity.get(verbosity, logging.DEBUG))
        journal_handler.setFormatter(self.__formatter)
        root_logger = logging.getLogger()
        root_logger.addHandler(journal_handler)
        logger.info(
            f"Journal handler with verbosity level {verbosity} added to logging"
        )
