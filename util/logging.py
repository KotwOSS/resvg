import sys
from .colors import *

# Logger class
class Logger:
    DEBUG = -1
    INFO = 0
    WARNING = 1
    ERROR = 2
    FATAL = 3

    # Shared logger
    logger = None

    def __init__(self, level, stream, silent):
        self.level = level
        self.stream = stream
        self.silent = silent

    def call(self, level, message):
        if self.level <= level:
            self.stream.write(message)

    def exit_fatal(self, message):
        self.fatal(message)
        if self.silent:
            sys.stderr.write(f"{remove_colors(message)}\n")
        sys.exit(1)



# CombinedLogger to combine multiple loggers
class CombinedLogger(Logger):
    def __init__(self, loggers):
        self.loggers = loggers

    def call(self, name, message):
        return [
            getattr(logger, name)(message) if logger else None
            for logger in self.loggers
        ]
    
    def exit_fatal(self, message):
        return self.call("exit_fatal", message)

    def debug(self, message):
        return self.call("debug", message)

    def info(self, message):
        return self.call("info", message)

    def warning(self, message):
        return self.call("warning", message)

    def error(self, message):
        return self.call("error", message)

    def fatal(self, message):
        return self.call("fatal", message)


# SimpleLogger for log files
class SimpleLogger(Logger):
    def debug(self, message):
        self.call(Logger.DEBUG, f"[DEBUG] {remove_colors(message)}\n")

    def info(self, message):
        self.call(Logger.INFO, f"[INFO] {remove_colors(message)}\n")

    def warning(self, message):
        self.call(Logger.WARNING, f"[WARNING] {remove_colors(message)}\n")

    def error(self, message):
        self.call(Logger.ERROR, f"[ERROR] {remove_colors(message)}\n")

    def fatal(self, message):
        self.call(Logger.FATAL, f"[FATAL] {remove_colors(message)}\n")


# PrettyLogger for stdout
class PrettyLogger(Logger):
    def debug(self, message):
        self.call(Logger.DEBUG, f"{gray}{bold}DEBUG{reset} {format_colors(message)}\n")

    def info(self, message):
        self.call(Logger.INFO, f"{blue}{bold}INFO{reset} {format_colors(message)}\n")

    def warning(self, message):
        self.call(
            Logger.WARNING, f"{yellow}{bold}WARNING{reset} {format_colors(message)}\n"
        )

    def error(self, message):
        self.call(Logger.ERROR, f"{red}{bold}ERROR{reset} {format_colors(message)}\n")

    def fatal(self, message):
        self.call(Logger.FATAL, f"{red}{bold}FATAL{reset} {format_colors(message)}\n")
