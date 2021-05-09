import logging

import constants


def get_logger(name=__name__):
    return logging.getLogger(name)


def init_logger(name=__name__):
    logging.basicConfig(
        level=constants.DEBUG_LEVEL,
        format="[%(asctime)s]"
        + "[%(pathname)s:%(lineno)s]"
        + "[%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    return get_logger(name)
