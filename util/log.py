import logging


def configure_logger():
    logging.basicConfig(
        format="[%(asctime)s]"
        + "[%(filename)s:%(funcName)s:%(lineno)s]"
        + "[%(levelname)8s]"
        + "%(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )


def get_logger():
    return logging.getLogger(__name__)
