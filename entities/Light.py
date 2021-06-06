import math
from typing import Any, Literal

import OpenGL.GL as gl

from entities.Car import Car
from entities.Entity import Entity
from renderer.uniform import LIGHT_COLOR, LIGHT_L, LIGHT_R, prepare_uniforms
from renderer.View import View
from shader.Shader import Shader
from shader.utils import create_vertex_obj, prepare_vertex_data_buffer
from utils.math import Mat4, create_sphere, make_rotation_y, make_translation


class Light(Entity):
    vertices = create_sphere(3)
    vertex_obj: Any
    shader: Shader
    car: Car

    position: Mat4

    def __init__(
        self,
        car: Car = None,
        position: Literal["L", "R"] = None,
    ):
        super().__init__(name="Sphere")
        assert car is not None
        assert position == "L" or position == "R"
        self.car = car

        if position == "L":
            self.position = LIGHT_L
        elif position == "R":
            self.position = LIGHT_R
        else:
            raise AssertionError(f"position '{position}' was not 'L' or 'R'")

        self.upload_data()

        self.shader = Shader(
            vertex_source_filename="sphere_vertex",
            fragment_source_filename="sphere_fragment",
        )

    def upload_data(self):
        self.vertex_obj = create_vertex_obj()
        prepare_vertex_data_buffer(self.vertex_obj, self.vertices, 0)
        prepare_vertex_data_buffer(self.vertex_obj, self.vertices, 1)

    def render(self, view: View = None):
        super().render(view=view)

        prepare_uniforms(
            program=self.shader.program,
            view=view,
            model_to_world_transform=make_translation(*self.car.position)
            * make_rotation_y(math.radians(self.car.drift_yaw))
            * self.position,
            light_position=self.car.position,
            uniform_overrides={"sphereColour": LIGHT_COLOR},
        )

        gl.glBindVertexArray(self.vertex_obj)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.vertices))
