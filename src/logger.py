from logging import Formatter, Logger, getLogger


def get_logger() -> Logger:
    return getLogger("my_logger")


def get_formatter() -> Formatter:
    return Formatter("%(asctime)s : %(levelname)s - %(message)s")
