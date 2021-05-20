import math
from typing import Tuple

import constants
from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import Mat4, make_translation, vec3


class Car(Entity):
    max = 10
    min = -10

    rotation = Mat4()
    position = [0, 1.5, 0]

    speed = 0.1

    def __init__(self):
        super().__init__(
            name="Car",
            filename="assets/camaro/Chevrolet_Camaro_SS_Low.obj",
        )

    def update(
        self,
        keyboard: Keyboard = None,
        mouse: Mouse = None,
        time: Time = None,
    ):
        super().update(keyboard=keyboard, mouse=mouse, time=time)

        # y is z in context of view
        x, z, y = self.position

        # horizontal movement
        if keyboard.state["A"]:
            x = min(x + self.speed, self.max)
        elif keyboard.state["D"]:
            x = max(x - self.speed, self.min)

        # vertical movement
        if keyboard.state["W"]:
            y = min(y + self.speed, self.max)
        elif keyboard.state["S"]:
            y = max(y - self.speed, self.min)

        self.position = (x, z, y)

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=self.rotation * make_translation(*self.position),
        )
