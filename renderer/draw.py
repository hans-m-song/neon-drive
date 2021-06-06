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


def prepare_uniforms(
    program: Any = None,
    view: View = None,
    light_position: list[float] = None,
    # TODO light_rotation: float = None
    model_to_world_transform: Mat4 = None,
    uniform_overrides: Dict[str, Any] = {},
):
    assert program is not None
    assert view is not None
    assert light_position is not None
    # TODO assert light_rotation is not None
    assert model_to_world_transform is not None

    model_to_view = view.world_to_view_transform * model_to_world_transform
    model_to_view_normal = inverse(transpose(Mat3(model_to_view)))
    model_to_clip: Mat4 = (
        view.view_to_clip_transform
        * view.world_to_view_transform
        * model_to_world_transform
    )

    gl.glUseProgram(program)

    uniforms = {
        "modelToClipTransform": model_to_clip,
        "modelToViewTransform": model_to_view,
        "modelToViewNormalTransform": model_to_view_normal,
        "viewSpaceLightDirection": [0.0, 0.0, -1.0],
        "lightColourAndIntensity": vec3(0.9, 0.9, 0.9),
        "ambientLightColourAndIntensity": vec3(0.1),
        "fogExtinctionOffset": 35.0,
        "fogExtinctionCoeff": 0.002,
        "fogColor": vec3(0.73),
        "enableSrgb": True,
    }

    uniforms.update(uniform_overrides)

    for key, value in uniforms.items():
        set_uniform(program, key, value)
