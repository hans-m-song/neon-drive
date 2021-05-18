from entities.Entity import Entity
from renderer.draw import draw_obj
from utils.math import Mat4


class Ground(Entity):
    def __init__(self):
        super().__init__(name="Ground", filename="assets/ground/ground.obj")

    def render(self, view=None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=Mat4(),
        )
