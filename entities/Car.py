import math
from renderer.View import View
from typing import Tuple
from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from utils.math import make_rotation_y, make_translation

import constants

MAX = 10
MIN = -10


class Car(Entity):
    position: Tuple[float, float, float] = (0.0, 1.5, 0.0)
    rotation = make_rotation_y(math.radians(180))

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

        # update x
        if keyboard.state["A"]:
            x = min(x + 1, MAX)
            if constants.DEBUG:
                print(f"Car left {x}")
        elif keyboard.state["D"]:
            x = max(x - 1, MIN)
            if constants.DEBUG:
                print(f"Car right {x}")

        # update y
        if keyboard.state["W"]:
            y = min(y + 1, MAX)
            if constants.DEBUG:
                print(f"Car up {y}")
        elif keyboard.state["S"]:
            y = max(y - 1, MIN)
            if constants.DEBUG:
                print(f"Car down {y}")

        self.position = (x, z, y)

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=self.rotation * make_translation(*self.position),
        )
