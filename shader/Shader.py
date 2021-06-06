from typing import Any, Dict

import OpenGL.GL as gl

from entities.ObjModel import ObjModel
from shader.utils import (
    Program,
    ShaderSource,
    Texture,
    build_shader,
    create_default_texture,
    load_glsl,
    set_uniform,
)
from utils.log import get_logger

logger = get_logger()


class Shader:
    texture: Texture
    texture_normal: Texture

    vertex_source: ShaderSource
    fragment_source: ShaderSource

    program: Program

    def __init__(
        self,
        vertex_source_filename: str = "default_vertex",
        fragment_source_filename: str = "default_fragment",
        vertex_attribute_overrides: Dict[str, Any] = {},
        fragment_attribute_overrides: Dict[str, Any] = {},
    ):
        self.texture = create_default_texture([1.0, 1.0, 1.0, 1.0])
        self.texture_normal = create_default_texture([0.5, 0.5, 0.5, 1.0])

        self.vertex_source = load_glsl(vertex_source_filename)
        self.fragment_source = load_glsl(fragment_source_filename)

        vertex_attributes = {}

        fragment_attributes = {}

        vertex_attributes.update(vertex_attribute_overrides)
        fragment_attributes.update(fragment_attribute_overrides)

        self.program = build_shader(
            self.vertex_source,
            self.fragment_source,
            attrib_locs=vertex_attributes,
            frag_data_locs=fragment_attributes,
        )

        self.use()

        default_bindings = {
            "diffuse_texture": ObjModel.TU_Diffuse,
            "opacity_texture": ObjModel.TU_Opacity,
            "specular_texture": ObjModel.TU_Specular,
            "normal_texture": ObjModel.TU_Normal,
        }
        for item, value in default_bindings.items():
            set_uniform(self.program, item, value)

        gl.glUseProgram(0)

        logger.debug(
            f"loaded shader: {vertex_source_filename}, {fragment_source_filename}"
        )

    def use(self):
        gl.glUseProgram(self.program)
