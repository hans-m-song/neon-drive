from typing import Any

import OpenGL.GL as gl
from PIL import Image

from entities.Entity import Entity
from renderer.uniform import prepare_uniforms
from renderer.View import View
from shader.Shader import Shader
from shader.utils import create_vertex_obj, prepare_vertex_data_buffer
from utils.log import get_logger
from utils.math import Mat4, make_scale, make_translation, vec3

logger = get_logger()


CUBE_VERTICES = [
    # 1
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, -1.0],
    [1.0, -1.0, -1.0],
    [1.0, -1.0, -1.0],
    [1.0, 1.0, -1.0],
    [-1.0, 1.0, -1.0],
    # 2
    [-1.0, -1.0, 1.0],
    [-1.0, -1.0, -1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, 1.0, 1.0],
    [-1.0, -1.0, 1.0],
    # 3
    [1.0, -1.0, -1.0],
    [1.0, -1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, -1.0],
    [1.0, -1.0, -1.0],
    # 4
    [-1.0, -1.0, 1.0],
    [-1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [1.0, -1.0, 1.0],
    [-1.0, -1.0, 1.0],
    # 5
    [-1.0, 1.0, -1.0],
    [1.0, 1.0, -1.0],
    [1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0],
    [-1.0, 1.0, 1.0],
    [-1.0, 1.0, -1.0],
    # 6
    [-1.0, -1.0, -1.0],
    [-1.0, -1.0, 1.0],
    [1.0, -1.0, -1.0],
    [1.0, -1.0, -1.0],
    [-1.0, -1.0, 1.0],
    [1.0, -1.0, 1.0],
]


def load_cube_textures() -> int:
    texture_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, texture_id)

    surfaces = {
        "posx": gl.GL_TEXTURE_CUBE_MAP_POSITIVE_X,
        "negx": gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_X,
        "posy": gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Y,
        "negy": gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Y,
        "posz": gl.GL_TEXTURE_CUBE_MAP_POSITIVE_Z,
        "negz": gl.GL_TEXTURE_CUBE_MAP_NEGATIVE_Z,
    }

    for surface, face_id in surfaces.items():
        path = f"assets/skybox/{surface}.dds"
        with Image.open(path).transpose(Image.FLIP_TOP_BOTTOM) as image:
            data = image.tobytes("raw", "RGBA", 0, -1)
            gl.glTexImage2D(
                face_id,
                0,
                gl.GL_RGBA,
                image.size[0],
                image.size[1],
                0,
                gl.GL_RGBA,
                gl.GL_UNSIGNED_BYTE,
                data,
            )

    gl.glGenerateMipmap(gl.GL_TEXTURE_CUBE_MAP)

    gl.glTexParameteri(
        gl.GL_TEXTURE_CUBE_MAP,
        gl.GL_TEXTURE_MAG_FILTER,
        gl.GL_LINEAR,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_CUBE_MAP,
        gl.GL_TEXTURE_MIN_FILTER,
        gl.GL_LINEAR_MIPMAP_LINEAR,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_WRAP_R,
        gl.GL_CLAMP_TO_EDGE,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_WRAP_S,
        gl.GL_CLAMP_TO_EDGE,
    )
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D,
        gl.GL_TEXTURE_WRAP_T,
        gl.GL_CLAMP_TO_EDGE,
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

    return texture_id


class CubeMap(Entity):
    vertex_obj: Any

    texture_id: int

    shader: Shader

    position: Mat4 = make_scale(400.0, 400.0, 400.0)

    def __init__(self):
        super().__init__("CubeMap")

        self.upload_data()

        self.texture_id = load_cube_textures()

        self.shader = Shader(
            vertex_source_filename="cubemap_vertex",
            fragment_source_filename="cubemap_fragment",
        )

        logger.debug("loaded cube map")

    def upload_data(self):
        self.vertex_obj = create_vertex_obj()
        prepare_vertex_data_buffer(self.vertex_obj, CUBE_VERTICES, 0)

    def use(self):
        gl.glActiveTexture(gl.GL_TEXTURE3)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture_id)

    def render(self, view: View = None):
        super().render(view=view)

        self.use()
        prepare_uniforms(
            program=self.shader.program,
            view=view,
            model_to_world_transform=self.position,
            light_position=vec3(0),
            light_rotation=vec3(0),
            uniform_overrides={
                "cubemap": 0,
                "fogColor": vec3(0.63),
            },
        )

        gl.glBindVertexArray(self.vertex_obj)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(CUBE_VERTICES))
        gl.glBindVertexArray(0)

        gl.glUseProgram(0)
