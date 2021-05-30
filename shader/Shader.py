from typing import Any, Dict

import OpenGL.GL as gl

from shader.utils import (
    build_shader,
    create_default_texture,
    load_glsl,
    set_uniform,
)


class Shader:

    RF_Transparent = 1
    RF_AlphaTested = 2
    RF_Opaque = 4
    RF_All = RF_Opaque | RF_AlphaTested | RF_Transparent

    AA_Position = 0
    AA_Normal = 1
    AA_TexCoord = 2
    AA_Tangent = 3
    AA_Bitangent = 4

    TU_Diffuse = 0
    TU_Opacity = 1
    TU_Specular = 2
    TU_Normal = 3
    TU_Max = 4

    texture: Any
    texture_normal: Any

    vertex_source_filename: str
    fragment_source_filename: str

    vertex_source: Any
    fragment_source: Any

    program: Any

    def __init__(
        self,
        vertex_source_filename: str = "default_vertex",
        fragment_source_filename: str = "default_fragment",
        attributes: Dict[str, Any] = {},
    ):
        self.texture = create_default_texture([1.0, 1.0, 1.0, 1.0])
        self.texture_normal = create_default_texture([0.5, 0.5, 0.5, 1.0])

        self.vertex_source_filename = vertex_source_filename
        self.fragment_source_filename = fragment_source_filename

        self.vertex_source = load_glsl(vertex_source_filename)
        self.fragment_source = load_glsl(fragment_source_filename)

        self.program = build_shader(
            self.vertex_source,
            self.fragment_source,
            attributes,
        )

    def use(self):
        gl.glUseProgram(self.program)

    def set_uniforms(self, uniforms: Dict[str, Any]):
        for item, value in uniforms.items():
            set_uniform(self.program, item, value)
