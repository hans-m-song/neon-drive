import math

from renderer.control import Mouse
from utils.math import (
    Mat3,
    Mat4,
    make_look_at,
    make_perspective,
    make_rotation_x,
    make_rotation_y,
    vec3,
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

    view_position = vec3(15.0, 15.0, 15.0)
    view_target = vec3(0.0, 0.0, 0.0)
    view_up = vec3(0.0, 1.0, 0.0)

    angle_yaw = 180
    angle_pitch = 20
    rotation = Mat4() * make_rotation_y(math.radians(135))

    # ignore the first tick to ignore mouse moving to (0, 0)
    first_tick = True

    mouse_move_scale = 0.05

    mouse: Mouse

    def __init__(self, mouse: Mouse = None) -> None:
        assert mouse is not None

        self.mouse = mouse

    def update(self, width, height) -> None:
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

        # TODO handle case when directly above

        self.angle_yaw -= delta_x * self.mouse_move_scale
        self.angle_pitch -= delta_y * self.mouse_move_scale

        yaw = Mat3(make_rotation_y(math.radians(self.angle_yaw)))
        pitch = Mat3(make_rotation_x(math.radians(-self.angle_pitch)))

        position = yaw * pitch * [0.0, 0.0, self.distance]

        self.world_to_view_transform = make_look_at(
            position,
            self.view_target,
            self.view_up,
        )
