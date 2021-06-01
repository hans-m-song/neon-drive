from typing import Any, Dict

import OpenGL.GL as gl

from entities.ObjModel import ObjModel
from renderer.View import View
from shader.utils import (
    Program,
    ShaderSource,
    Texture,
    build_shader,
    create_default_texture,
    load_glsl,
    set_uniform,
)
from utils.math import Mat3, Mat4, inverse, transform_point, transpose, vec3


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
        attribute_overrides: Dict[str, Any] = {},
    ):
        self.texture = create_default_texture([1.0, 1.0, 1.0, 1.0])
        self.texture_normal = create_default_texture([0.5, 0.5, 0.5, 1.0])

        self.vertex_source = load_glsl(vertex_source_filename)
        self.fragment_source = load_glsl(fragment_source_filename)

        attributes = {
            "positionAttribute": ObjModel.AA_Position,
            "normalAttribute": ObjModel.AA_Normal,
            "texCoordAttribute": ObjModel.AA_TexCoord,
            "tangentAttribute": ObjModel.AA_Tangent,
            "bitangentAttribute": ObjModel.AA_Bitangent,
        }

        attributes.update(attribute_overrides)

        self.program = build_shader(
            self.vertex_source,
            self.fragment_source,
            attributes,
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

    def use(self):
        gl.glUseProgram(self.program)

    def set_uniforms(
        self,
        view: View = None,
        model_to_world_tranform: Mat4 = None,
        uniform_overrides: Dict[str, Any] = {},
    ):
        assert view is not None
        assert model_to_world_tranform is not None

        model_to_clip_transform = (
            view.view_to_clip_transform
            * view.world_to_view_transform
            * model_to_world_tranform
        )

        model_to_view_transform = (
            view.world_to_view_transform * model_to_world_tranform
        )

        model_to_view_normal_transform = inverse(
            transpose(Mat3(model_to_view_transform))
        )

        uniforms = {}

        vertex_uniforms = {
            "modelToClipTransform": model_to_clip_transform,
            "modelToViewTransform": model_to_view_transform,
            "modelToViewNormalTransform": model_to_view_normal_transform,
            "viewToClipTransform": view.view_to_clip_transform,
            "worldToViewTransform": view.world_to_view_transform,
        }

        fragment_uniforms = {
            "viewSpaceLightPosition": transform_point(
                view.world_to_view_transform, vec3(0)
            ),
            "lightColourAndIntensity": vec3(0.9, 0.9, 0.9),
            "ambientLightColourAndIntensity": vec3(0.1),
            "viewToWorldRotationTransform": inverse(
                Mat3(view.world_to_view_transform)
            ),
            "fogExtinctionCoeff": 0.05,
        }

        uniforms.update(
            vertex_uniforms,
        )
        uniforms.update(fragment_uniforms)
        uniforms.update(uniform_overrides)

        for item, value in uniforms.items():
            set_uniform(self.program, item, value)
