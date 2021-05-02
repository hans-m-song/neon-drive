import logging

import constants


def get_logger():
    return logging.getLogger()


def init_logger():
    logging.basicConfig(
        level=constants.DEBUG_LEVEL,
        format="[%(asctime)s]"
        + "[%(pathname)s:%(funcName)s:%(lineno)s]"
        + "[%(levelname)8s] %(message)s",
        datefmt="%H:%M:%S",
    )
    return get_logger()
