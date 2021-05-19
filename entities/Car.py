import math
from entities.Entity import Entity
from entities.Ground import Ground
from renderer.control import KEY_MAP, Keyboard, Mouse, Time
from renderer.draw import draw_obj
from utils.math import make_rotation_y, make_translation, vec3
import constants

MAX = 10
MIN = -10


class Car(Entity):
    position = vec3(0.0, 1.5, 0.0)

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

    def render(self, view=None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=make_rotation_y(math.radians(180))
            * make_translation(*self.position),
        )
