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
from utils.log import get_logger
from utils.math import Mat3, Mat4, inverse, transform_point, transpose, vec3

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

    def set_uniforms(
        self,
        view: View = None,
        model_to_world_tranform: Mat4 = None,
        uniform_overrides: Dict[str, Any] = {},
        use_defaults=True,
    ):
        assert view is not None
        assert model_to_world_tranform is not None

        model_to_clip_transform: Mat4 = (
            view.view_to_clip_transform
            * view.world_to_view_transform
            * model_to_world_tranform
        )

        model_to_view_transform: Mat4 = (
            view.world_to_view_transform * model_to_world_tranform
        )

        model_to_view_normal_transform: Mat3 = inverse(
            transpose(Mat3(model_to_view_transform))
        )

        view_space_light_position: Mat4 = transform_point(
            view.world_to_view_transform, vec3(0)
        )

        uniforms = {}

        if use_defaults:
            vertex_uniforms = {
                "modelToClipTransform": model_to_clip_transform,
                "modelToViewTransform": model_to_view_transform,
                "modelToViewNormalTransform": model_to_view_normal_transform,
                "worldToViewTransform": view.world_to_view_transform,
                "viewToClipTransform": view.view_to_clip_transform,
                "viewPosition": view.position,
            }

            print(view.position)

            fragment_uniforms = {
                "viewSpaceLightPosition": view_space_light_position,
                "lightColourAndIntensity": vec3(0.9, 0.9, 0.9),
                "ambientLightColourAndIntensity": vec3(0.1),
                "fogExtinctionCoeff": 0.5,
                "fogColor": vec3(0.73),
            }

            uniforms.update(vertex_uniforms)
            uniforms.update(fragment_uniforms)

        uniforms.update(uniform_overrides)

        for item, value in uniforms.items():
            set_uniform(self.program, item, value)
