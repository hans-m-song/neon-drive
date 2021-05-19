import logging
import os


def get_log_level():
    log_level = os.environ.get("DEBUG_LEVEL", "INFO").upper()
    if log_level == "CRITICAL":
        return logging.CRITICAL
    if log_level == "ERROR":
        return logging.ERROR
    if log_level == "WARNING":
        return logging.WARNING
    if log_level == "INFO":
        return logging.INFO
    if log_level == "DEBUG":
        return logging.DEBUG
    if log_level == "NOTSET":
        return logging.NOTSET
    if log_level == "DEBUG":
        return logging.DEBUG
    else:
        return logging.INFO


def get_env_bool(key: str, default: str = "true"):
    return os.environ.get(key, default).lower() == "true"


DEBUG = get_env_bool("DEBUG")
DEBUG_LEVEL = logging.DEBUG  # get_log_level()

WINDOW_NAME = "NEON DRIVE"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SKIP_ASSET_LOAD = get_env_bool("SKIP_ASSET_LOAD", "false")

CAPTURE_MOUSE = False  # get_env_bool("CAPTURE_MOUSE")

TARGET_FPS = 120
