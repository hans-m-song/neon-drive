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
    vec3,
)

DEFAULT_VIEW_OFFSET = [0, 0]
DEFAULT_VIEW_TARGET = [0.0, 0.0, 0.0]
DEFAULT_ANGLE_YAW = 180
DEFAULT_ANGLE_PITCH = 20


class View:
    width = 0
    height = 0
    aspect_ratio = 0

    fov = 60.0
    distance_near = 0.2
    distance_far = 2000.0

    view_to_clip_transform = Mat4()
    world_to_view_transform = Mat4()

    view_offset = DEFAULT_VIEW_OFFSET
    view_target = DEFAULT_VIEW_TARGET
    view_up = [0.0, 1.0, 0.0]

    angle_yaw = DEFAULT_ANGLE_YAW
    angle_pitch = DEFAULT_ANGLE_PITCH
    rotation = Mat4() * make_rotation_y(math.radians(135))

    # ignore the first tick to ignore mouse moving to (0, 0)
    first_tick = True

    mouse_move_scale = 0.05
    camera_translate_scale = 0.1

    max = 10
    min = -10

    mouse: Mouse
    keyboard: Keyboard

    def __init__(self, mouse: Mouse = None, keyboard: Keyboard = None) -> None:
        assert mouse is not None
        assert keyboard is not None

        self.mouse = mouse
        self.keyboard = keyboard

    def calculate_offset(self):
        x, y = self.view_offset

        # horizontal movement
        if self.keyboard.state["LEFT"]:
            x = x + self.camera_translate_scale
        elif self.keyboard.state["RIGHT"]:
            x = x - self.camera_translate_scale

        # vertical movement
        if self.keyboard.state["UP"]:
            y = min(y + self.camera_translate_scale, 20)
        elif self.keyboard.state["DOWN"]:
            y = max(y - self.camera_translate_scale, -5)

        return [x, y]

    def calculate_angle(self):
        delta_x, delta_y = self.mouse.delta

        if self.first_tick:
            delta_x, delta_y = (0, 0)
            self.first_tick = False

        angle_yaw = self.angle_yaw - delta_x * self.mouse_move_scale
        angle_pitch = clamp(
            self.angle_pitch + delta_y * self.mouse_move_scale,
            limit_min=1,
            limit_max=89,
        )

        yaw = Mat3(make_rotation_y(math.radians(angle_yaw)))
        pitch = Mat3(make_rotation_x(math.radians(-angle_pitch)))
        angle = yaw * pitch

        return (angle_yaw, angle_pitch, angle)

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

        if self.keyboard.state["MOUSE_BUTTON_MIDDLE"]:
            self.view_offset = DEFAULT_VIEW_OFFSET
            self.view_target = DEFAULT_VIEW_TARGET
            self.angle_yaw = DEFAULT_ANGLE_YAW
            self.angle_pitch = DEFAULT_ANGLE_PITCH

        self.angle_yaw, self.angle_pitch, angle = self.calculate_angle()
        self.view_offset = self.calculate_offset()

        offset = vec3(*self.view_offset)
        position = offset + (angle * [0, 0, 20])
        target = self.view_target if not view_target else view_target.position
        offset_target = vec3(*target) + offset

        self.world_to_view_transform = make_look_at(
            position,
            offset_target,
            self.view_up,
        )
