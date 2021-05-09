from entities.Entity import Entity
from utils.lab_utils import vec3


class Car(Entity):
    position = vec3(0, 0, 0)
    velocity = vec3(0, 0, 0)
    direction = vec3(1, 0, 0)
    speed = 0.0

    def __init__(self):
        super().__init__(name="Car", filename="assets/car/BMW850.obj")
