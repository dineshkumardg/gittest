import logging
import sys


# singleton
class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name, log_level):
        if cls._logger is None:
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(log_level)  # FATAL > ERROR > WARNING > INFO > DEBUG
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(
                logging.Formatter("%(asctime)s: %(levelname)s: %(funcName)s, %(lineno)s: %(message)s"))  # %(funcName)s,
            cls._logger.addHandler(handler)
        return cls._logger
