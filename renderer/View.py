from renderer.control import Mouse
from utils.math import Mat4, make_look_at, make_perspective

# x - rotation
# y - tilt
# z - distance to model
DEFAULT_VIEW_POSITION = [10.0, 10.0, 20.0]


class View:
    width = 0
    height = 0
    aspect_ratio = 0

    fov = 60.0
    distance_near = 0.2
    distance_far = 2000.0

    view_to_clip_transform = Mat4()
    world_to_view_transform = Mat4()

    view_position = DEFAULT_VIEW_POSITION
    view_target = [0.0, 0.0, 0.0]
    view_up = [0.0, 1.0, 0.0]

    mouse: Mouse = None

    def __init__(self, mouse: Mouse = None):
        """
        kwargs:
            mouse: Mouse
        """
        assert mouse is not None

        self.mouse = mouse

    def update(self, width, height):
        self.width = width
        self.height = height
        self.aspect_ratio = float(width) / float(height)

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
