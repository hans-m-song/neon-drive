import math
from typing import Any

import OpenGL.GL as gl

from entities.Entity import Entity
from renderer.View import View
from shader.Shader import Shader
from shader.Texture import Texture
from shader.utils import create_vertex_obj, prepare_vertex_data_buffer
from utils.math import Mat4, make_rotation_x, make_scale

SQUARE_VERTS = [
    [-0.9, 0.9, 0],
    [-0.9, -0.9, 0],
    [0.9, -0.9, 0],
    [0.9, 0.9, 0],
]

TEXTURE_COORDINATES = [
    [0, 1],
    [0, 0],
    [1, 0],
    [1, 1],
]


class Ground(Entity):
    rotation = Mat4()
    size = 4
    scale = 1
    height = 0

    vertices = SQUARE_VERTS
    vertex_obj: Any
    shader: Shader
    texture: Texture

    def __init__(self):
        super().__init__(name="Ground")

        self.upload_data()
        # TODO tile textures?
        # TODO translate textures?
        self.texture = Texture("road/tarmac-square.png")
        self.shader = Shader(attribute_overrides={})

    def upload_data(self):
        self.vertex_obj = create_vertex_obj()
        prepare_vertex_data_buffer(self.vertex_obj, SQUARE_VERTS, 0)
        prepare_vertex_data_buffer(self.vertex_obj, TEXTURE_COORDINATES, 1)

    def render(self, view: View = None):
        super().render(view=view)

        gl.glBindVertexArray(self.vertex_obj)
        self.texture.use()
        self.shader.use()

        self.shader.set_uniforms(
            view=view,
            model_to_world_tranform=Mat4()
            * make_rotation_x(math.radians(90))
            * make_scale(10, 10, 1),
            uniform_overrides={"tex": 0, "texCoordScale": 10.01},
        )

        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, len(SQUARE_VERTS))

        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
