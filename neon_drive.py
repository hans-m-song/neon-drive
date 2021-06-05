import constants
from entities.Car import Car
from entities.Ground import Ground
from entities.Treadmill import Treadmill
from renderer.Engine import Engine
from utils.log import init_logger


def load_assets(engine: Engine):
    car = Car()
    ground = Ground()
    treadmill_parts = [
        Treadmill(
            car=car,
            position=i,
            count=20,
        )
        for i in range(20)
    ]

    engine.add_resource(car, view_target=True)
    engine.add_resource(ground)
    for part in treadmill_parts:
        engine.add_resource(part)


def run():
    logger = init_logger()
    logger.info("Starting neon drive...")

    engine = Engine()

    if not constants.SKIP_ASSET_LOAD:
        load_assets(engine)

    engine.run()


if __name__ == "__main__":
    run()
