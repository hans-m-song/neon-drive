from typing import Any

import OpenGL.GL as gl
from PIL import Image

from entities.Entity import Entity
from entities.ObjModel import ObjModel
from renderer.View import View
from shader.Shader import Shader
from shader.utils import (
    create_vertex_obj,
    prepare_vertex_data_buffer,
    set_uniform,
)
from utils.log import get_logger
from utils.math import Mat4

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
    gl.glActiveTexture(gl.GL_TEXTURE0)
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
        path = f"assets/skybox/{surface}.png"
        with Image.open(path).transpose(Image.FLIP_TOP_BOTTOM) as image:
            data = image.tobytes("raw", "RGBX", 0, -1)
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
        gl.GL_TEXTURE_CUBE_MAP, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR
    )

    gl.glTexParameteri(
        gl.GL_TEXTURE_CUBE_MAP,
        gl.GL_TEXTURE_MIN_FILTER,
        gl.GL_LINEAR_MIPMAP_LINEAR,
    )

    return texture_id


class CubeMap(Entity):
    vertex_obj: Any

    texture_id: int

    shader: Shader

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

    def use(self, shader):
        # set_uniform(shader, "environmentCubeTexture", ObjModel.TU_EnvMap)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_CUBE_MAP, self.texture_id)

    def render(self, view: View = None):
        super().render(view=view)

        self.use()
        self.shader.use()

        self.shader.set_uniforms(
            view=view,
            model_to_world_tranform=Mat4(),
            uniform_overrides={
                "cubemap": 0,
                "texCoordScale": 5.0,
                "viewPosition": view.position,
            },
        )

        gl.glBindVertexArray(self.vertex_obj)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(CUBE_VERTICES))
        gl.glBindVertexArray(0)

        gl.glUseProgram(0)
