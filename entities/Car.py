import math

from entities.Entity import Entity
from renderer.control import Keyboard, Mouse, Time
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import clamp, make_rotation_y, make_translation


class Car(Entity):
    position = [0, 1.6, 0]
    drift_yaw = 0

    move_speed = 0.1
    strafe_speed = 0.05
    drift_speed = 0.4
    return_speed = 0.01
    velocity = 0.2
    acceleration = 0.05

    velocity_min = 0.1
    velocity_max = 0.8
    offset_max = 5
    offset_min = -5
    yaw_max = 35
    yaw_min = -35

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
        yaw = self.drift_yaw

        # horizontal movement
        if keyboard.state["A"]:
            x = min(x + self.strafe_speed, self.offset_max)
            yaw = clamp(
                yaw + self.drift_speed,
                limit_max=self.yaw_max,
                limit_min=self.yaw_min,
            )
        elif keyboard.state["D"]:
            x = max(x - self.strafe_speed, self.offset_min)
            yaw = clamp(
                yaw - self.drift_speed,
                limit_max=self.yaw_max,
                limit_min=self.yaw_min,
            )

        # vertical movement
        if keyboard.state["W"]:
            y = min(y + self.move_speed, self.offset_max)
            self.velocity = clamp(
                self.velocity + self.acceleration,
                limit_max=self.velocity_max,
                limit_min=self.velocity_min,
            )
        elif keyboard.state["S"]:
            y = max(y - self.move_speed, self.offset_min)
            self.velocity = clamp(
                self.velocity - self.acceleration,
                limit_max=self.velocity_max,
                limit_min=self.velocity_min,
            )

        # eventually return to center
        if y > 0:
            y = max(y - self.return_speed, 0)
        elif y < 0:
            y = min(y + self.return_speed, 0)

        if x > 0:
            x = max(x - self.return_speed, 0)
        elif x < 0:
            x = min(x + self.return_speed, 0)

        if yaw > 0:
            yaw = max(yaw - 10 * self.return_speed, 0)
        elif yaw < 0:
            yaw = min(yaw + 10 * self.return_speed, 0)

        self.drift_yaw = yaw
        self.position = [x, z, y]

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=make_translation(*self.position)
            * make_rotation_y(math.radians(self.drift_yaw)),
            uniform_overrides={"viewPosition": view.position},
        )
