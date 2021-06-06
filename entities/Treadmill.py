import math

from entities.Car import Car
from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import make_rotation_y, make_scale, make_translation, vec3


class Treadmill(Entity):
    model_to_world = make_scale(8, 2, 2)

    position = 0
    scaling = 21
    range: int
    offset: int

    car: Car

    def __init__(self, car: Car = None, position: int = 0, count: int = 1):
        super().__init__(name="Ground", filename="assets/bridge/brije.obj")
        assert car is not None
        assert position > -1

        self.car = car
        self.position = position * self.scaling
        self.range = count * self.scaling
        self.offset = self.range / 2

    def update(
        self,
        keyboard: Keyboard = None,
        mouse: Mouse = None,
        time: Time = None,
    ):
        super().update(keyboard=keyboard, mouse=mouse, time=time)

        self.position = (self.position + self.car.velocity) % self.range

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=self.model_to_world
            * make_translation(0.5, -1.8, -self.position + self.offset)
            * make_rotation_y(math.radians(90)),
        )
