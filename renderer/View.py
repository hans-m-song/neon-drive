import math

from renderer.control import Keyboard, Mouse
from utils.math import (
    Mat3,
    Mat4,
    clamp,
    make_look_at,
    make_perspective,
    make_rotation_x,
    make_rotation_y,
)


class View:
    width = 0
    height = 0
    aspect_ratio = 0

    fov = 60.0
    distance_near = 0.2
    distance = 20
    distance_far = 2000.0

    view_to_clip_transform = Mat4()
    world_to_view_transform = Mat4()

    view_target = [0.0, 0.0, 0.0]
    view_up = [0.0, 1.0, 0.0]

    angle_yaw = 180
    angle_pitch = 20
    rotation = Mat4() * make_rotation_y(math.radians(135))

    # ignore the first tick to ignore mouse moving to (0, 0)
    first_tick = True

    mouse_move_scale = 0.05

    max = 10
    min = -10

    mouse: Mouse
    keyboard: Keyboard

    def __init__(self, mouse: Mouse = None) -> None:
        assert mouse is not None

        self.mouse = mouse

    def update(self, width, height, view_target=None) -> None:
        self.width = width
        self.height = height
        self.aspect_ratio = float(width) / float(height)

        self.view_to_clip_transform = make_perspective(
            self.fov,
            self.aspect_ratio,
            self.distance_near,
            self.distance_far,
        )

        delta_x, delta_y = self.mouse.delta

        if self.first_tick:
            delta_x, delta_y = (0, 0)
            self.first_tick = False

        self.angle_yaw -= delta_x * self.mouse_move_scale
        self.angle_pitch = clamp(
            self.angle_pitch + delta_y * self.mouse_move_scale,
            limit_min=1,
            limit_max=89,
        )

        yaw = Mat3(make_rotation_y(math.radians(self.angle_yaw)))
        pitch = Mat3(make_rotation_x(math.radians(-self.angle_pitch)))

        position = yaw * pitch * [0.0, 0.0, self.distance]

        self.world_to_view_transform = make_look_at(
            position,
            self.view_target if not view_target else view_target.position,
            self.view_up,
        )
