# Created on Wed May 25 2022
#
# Copyright (c) 2022 KotwOSS

import logging
import colors

fmt = "%(levelname)s >>§R  %(message)s"


class PrettyFormatter(logging.Formatter):
    levelnames = {
        logging.DEBUG: f"{colors.bold}{colors.gray}DEBUG   ",
        logging.INFO: f"{colors.bold}{colors.blue}INFO    ",
        logging.WARNING: f"{colors.bold}{colors.yellow}WARNING ",
        logging.ERROR: f"{colors.bold}{colors.red}ERROR   ",
        logging.CRITICAL: f"{colors.bold}{colors.dark_red}CRITICAL{colors.reset}{colors.red}",
    }

    def __init__(self, fmt):
        super().__init__(fmt)

    def format(self, record):
        record.levelname = PrettyFormatter.levelnames[record.levelno]
        return colors.format_colors(super().format(record)) + colors.reset


class SimpleFormatter(logging.Formatter):
    levelnames = {
        logging.DEBUG: "[DEBUG]   ",
        logging.INFO: "[INFO]    ",
        logging.WARNING: "[WARNING] ",
        logging.ERROR: "[ERROR]   ",
        logging.CRITICAL: "[CRITICAL]",
    }

    def __init__(self, fmt):
        super().__init__(fmt)

    def format(self, record):
        record.levelname = SimpleFormatter.levelnames[record.levelno]
        return colors.remove_colors(super().format(record))


def setup_logger(level: int, stdout: bool = True, file: str | None = None):
    logger = logging.getLogger()
    logger.setLevel(level)

    if stdout:
        stdout_handler = logging.StreamHandler()
        stdout_handler.setLevel(level)
        stdout_handler.setFormatter(PrettyFormatter(fmt))
        logger.addHandler(stdout_handler)

    if file:
        file_handler = logging.FileHandler(file)
        file_handler.setLevel(level)
        file_handler.setFormatter(SimpleFormatter(fmt))
        logger.addHandler(file_handler)
