import constants
from render import draw_ui, init_resources, render_frame, update
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
        init_resources,
        draw_ui,
        update,
    )


if __name__ == "__main__":
    run()
