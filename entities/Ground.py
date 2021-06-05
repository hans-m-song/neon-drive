import math
from typing import Any

import OpenGL.GL as gl

from entities.Entity import Entity
from renderer.View import View
from shader.Shader import Shader
from shader.Texture import Texture
from shader.utils import create_vertex_obj, prepare_vertex_data_buffer
from utils.math import make_scale

SQUARE_VERTS = [
    [-1, 0, -1],
    [-1, 0, 1],
    [1, 0, 1],
    [1, 0, -1],
]

TEXTURE_COORDINATES = [
    [0, 1],
    [1, 1],
    [1, 0],
    [0, 0],
]


def set_texture_parameters():
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_WRAP_S,
        gl.GL_REPEAT,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_WRAP_T,
        gl.GL_REPEAT,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_MAG_FILTER,
        gl.GL_LINEAR,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_MIN_FILTER,
        gl.GL_LINEAR,
    )


class Ground(Entity):
    vertex_obj: Any
    shader: Shader
    texture: Texture

    def __init__(self):
        super().__init__(name="Ground")

        self.upload_data()

        self.texture = Texture(
            "road/tarmac-plain.png",
            set_parameters=set_texture_parameters,
            mode="RGBX",
        )

        self.shader = Shader(
            vertex_source_filename="ground_vertex",
            fragment_source_filename="ground_fragment",
        )

    def upload_data(self):
        self.vertex_obj = create_vertex_obj()
        prepare_vertex_data_buffer(self.vertex_obj, SQUARE_VERTS, 0)
        prepare_vertex_data_buffer(self.vertex_obj, TEXTURE_COORDINATES, 1)

    def render(self, view: View = None):
        super().render(view=view)

        self.texture.use()
        self.shader.use()

        self.shader.set_uniforms(
            view=view,
            model_to_world_tranform=make_scale(150, 1, 150),
            uniform_overrides={
                "groundTexture": 0,
                "texCoordScale": 10.0,
                "fogExtinctionOffset": 35.0,
                "fogExtinctionCoeff": 0.006,
            },
        )

        gl.glBindVertexArray(self.vertex_obj)
        gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, len(SQUARE_VERTS))
        gl.glBindVertexArray(0)

        gl.glUseProgram(0)
