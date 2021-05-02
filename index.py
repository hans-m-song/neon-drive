import constants
from render import render_frame
from utils.log import init_logger
from utils.magic import runProgram


def run():
    logger = init_logger()
    logger.debug("Starting neon drive...")
    runProgram(
        constants.WINDOW_NAME,
        constants.WINDOW_WIDTH,
        constants.WINDOW_HEIGHT,
        render_frame,
    )


if __name__ == "__main__":
    run()
