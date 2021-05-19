import math

from renderer.control import Mouse
from utils.math import Mat4, clamp, make_look_at, make_perspective


class View:
    width = 0
    height = 0
    aspect_ratio = 0

    fov = 60.0
    distance_near = 0.2
    distance_far = 2000.0

    view_to_clip_transform = Mat4()
    world_to_view_transform = Mat4()

    # view_position = [rotation, tilt, distance to model]
    view_position = [10.0, 10.0, 20.0]
    view_target = [0.0, 0.0, 0.0]
    view_up = [0.0, 1.0, 0.0]

    y_max = 20.0
    y_min = 2.0
    x_max = 15.0
    x_min = -15.0

    phi = 0.0  # azimuth
    theta = 0.0  # incline
    orbit_radius = 20

    mouse_move_scale = 0.1

    mouse: Mouse

    def __init__(self, mouse: Mouse = None) -> None:
        """
        kwargs:
            mouse: Mouse
        """
        assert mouse is not None

        self.mouse = mouse

    def update(self, width, height) -> None:
        self.width = width
        self.height = height
        self.aspect_ratio = float(width) / float(height)

        delta_x, delta_y = self.mouse.delta
        old_x, old_y, old_z = self.view_position

        clamped_x, clamped_y = old_x, old_y

        # update x if changed
        if delta_x != 0:
            clamped_x = clamp(
                old_x - delta_x * self.mouse_move_scale,
                limit_max=self.x_max,
                limit_min=self.x_min,
            )

            self.phi = math.atan(abs(clamped_x) / old_z)
            scaled_x = self.orbit_radius * math.sin(self.phi)

            # maintain negative bearing if any
            if clamped_x < 0:
                scaled_x = scaled_x * -1

            self.view_position[0] = scaled_x

        # # update y if changed
        if delta_y != 0:
            clamped_y = clamp(
                old_y + delta_y * self.mouse_move_scale,
                limit_max=self.y_max,
                limit_min=self.y_min,
            )

            self.theta = math.atan(abs(clamped_y) / old_z)
            self.view_position[1] = self.orbit_radius * math.sin(self.theta)

            print(old_y, clamped_y, self.view_position[1])
            self.view_position[1] = clamped_y

        # update z if x or y changed
        if delta_x != 0 or delta_y != 0:
            self.view_position[2] = self.orbit_radius * math.cos(self.phi)

        self.view_to_clip_transform = make_perspective(
            self.fov,
            self.aspect_ratio,
            self.distance_near,
            self.distance_far,
        )

        self.world_to_view_transform = make_look_at(
            self.view_position,
            self.view_target,
            self.view_up,
        )
