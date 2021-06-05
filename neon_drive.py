import constants
from entities.Car import Car
from entities.CubeMap import CubeMap
from entities.Ground import Ground
from entities.Light import Light
from entities.Treadmill import Treadmill
from renderer.Engine import Engine
from utils.log import init_logger


def load_assets(engine: Engine):
    cubemap = CubeMap()
    car = Car()
    lightL = Light(cubemap=cubemap, car=car, position="L")
    lightR = Light(cubemap=cubemap, car=car, position="R")
    ground = Ground(cubemap=cubemap, car=car)
    treadmill_parts = [
        Treadmill(car=car, cubemap=cubemap, position=i, count=6)
        for i in range(6)
    ]

    engine.add_resource(lightL)
    engine.add_resource(lightR)
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
