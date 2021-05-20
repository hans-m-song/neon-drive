import constants
from entities.Car import Car
from entities.Ground import Ground
from renderer.Engine import Engine
from utils.log import init_logger


def run():
    logger = init_logger()
    logger.info("Starting neon drive...")

    engine = Engine()

    if not constants.SKIP_ASSET_LOAD:
        ground = Ground()
        car = Car()

        engine.add_resource(ground)
        engine.add_resource(car, view_target=True)

    engine.run()


if __name__ == "__main__":
    run()
