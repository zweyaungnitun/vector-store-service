import logging
import sys
import json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "time": self.formatTime(record, self.datefmt),
        }

        if hasattr(record, "extra_data"):
            log_record.update(record.extra_data)

        return json.dumps(log_record)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())

        logger.addHandler(handler)
        logger.propagate = False

    return logger