from typing import Any, Dict

import OpenGL.GL as gl

from entities.ObjModel import ObjModel
from renderer.View import View
from shader.utils import set_uniform
from utils.math import (
    Mat3,
    Mat4,
    inverse,
    make_scale,
    make_translation,
    transpose,
    vec3,
)

LIGHT_COLOR = vec3(1, 0.98, 0.67)
LIGHT_SCALE = make_scale(0.2, 0.2, 0.2)
LIGHT_TRANSLATE_L = make_translation(-7.2, -0.85, 23)
LIGHT_TRANSLATE_R = make_translation(7.2, -0.85, 23)
LIGHT_L = LIGHT_SCALE * LIGHT_TRANSLATE_L
LIGHT_R = LIGHT_SCALE * LIGHT_TRANSLATE_R


def draw_obj(
    model: ObjModel = None,
    view: View = None,
    light_position: list[float] = None,
    # TODO light_rotation: float = None
    model_to_world: Mat4 = None,
    shader: Any = None,
    uniform_overrides: Dict[str, Any] = {},
):
    assert model is not None
    assert view is not None
    assert light_position is not None
    # TODO assert light_rotation is not None
    assert model_to_world is not None

    model_to_view = view.world_to_view_transform * model_to_world
    model_to_view_normal = inverse(transpose(Mat3(model_to_view)))

    program = shader or model.defaultShader

    gl.glUseProgram(program)

    transforms = {
        "modelToClipTransform": view.view_to_clip_transform
        * view.world_to_view_transform
        * model_to_world,
        "modelToViewTransform": model_to_view,
        "modelToViewNormalTransform": model_to_view_normal,
    }

    uniforms = {
        "viewSpaceLightDirection": [0.0, 0.0, -1.0],
        "fogExtinctionOffset": 35.0,
        "fogExtinctionCoeff": 0.002,
        "fogColor": vec3(0.73),
        "enableSrgb": True,
        "origin": vec3(0),
    }

    uniforms.update(uniform_overrides)

    for key, value in uniforms.items():
        set_uniform(program, key, value)

    model.render(
        shaderProgram=program,
        transforms=transforms,
    )
