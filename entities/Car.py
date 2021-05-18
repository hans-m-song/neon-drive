from entities.Entity import Entity
from entities.Ground import Ground
from renderer.draw import draw_obj
from utils.math import make_translation, vec3


class Car(Entity):
    position = vec3(0, 1, 0)
    velocity = vec3(0, 0, 0)
    direction = vec3(1, 0, 0)
    speed = 0.0

    ground = None

    def __init__(self, ground: Ground = None):
        """
        kwargs:
            ground: Ground
        """
        assert ground is not None

        super().__init__(
            name="Car",
            filename="assets/camaro/Chevrolet_Camaro_SS_Low.obj",
        )

    def render(self, view=None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=make_translation(5.0, 5.0, 5.0),
        )
