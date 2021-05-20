from entities.Entity import Entity
from renderer.draw import draw_obj
from renderer.View import View
from utils.math import Mat4


class Ground(Entity):
    rotation = Mat4()

    def __init__(self):
        super().__init__(name="Ground", filename="assets/ground/ground.obj")

    def render(self, view: View = None):
        super().render(view=view)

        draw_obj(
            model=self.model,
            view=view,
            model_to_world=self.rotation,
        )
