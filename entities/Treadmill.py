from entities.Car import Car
from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import Mat4, make_scale, make_translation


class Treadmill(Entity):
    model_to_world = make_scale(3.5, 1, 2)
    position = 0

    range = 40
    offset = 20
    scaling = 8

    car: Car

    def __init__(self, car: Car = None, position: int = 0):
        super().__init__(name="Ground", filename="assets/road/road.obj")
        assert car is not None
        assert position > -1

        self.car = car
        self.position = position * self.scaling

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
            * make_translation(0, 0, -self.position + self.offset),
        )
