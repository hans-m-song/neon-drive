from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import clamp, make_translation


class Car(Entity):
    max = 10
    min = -10

    position = [0, 1.6, 0]

    move_speed = 0.1
    velocity = 0.2
    acceleration = 0.05

    velocity_min = 0.1
    velocity_max = 0.8

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
            x = min(x + self.move_speed, self.max)
        elif keyboard.state["D"]:
            x = max(x - self.move_speed, self.min)

        # vertical movement
        if keyboard.state["W"]:
            y = min(y + self.move_speed, self.max)
            self.velocity = clamp(
                self.velocity + self.acceleration,
                limit_max=self.velocity_max,
                limit_min=self.velocity_min,
            )
        elif keyboard.state["S"]:
            y = max(y - self.move_speed, self.min)
            self.velocity = clamp(
                self.velocity - self.acceleration,
                limit_max=self.velocity_max,
                limit_min=self.velocity_min,
            )

        self.position = (x, z, y)

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=make_translation(*self.position),
        )
