from typing import Any, Dict

import OpenGL.GL as gl

from renderer.View import View
from shader.utils import set_uniform
from utils.math import (
    Mat3,
    Mat4,
    inverse,
    make_scale,
    make_translation,
    transform_point,
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
    light_rotation: float = None,
    model_to_world_transform: Mat4 = None,
    uniform_overrides: Dict[str, Any] = {},
    verbose: str = None,
):
    assert program is not None
    assert view is not None
    assert light_position is not None
    assert light_rotation is not None
    assert model_to_world_transform is not None

    model_to_view = view.world_to_view_transform * model_to_world_transform
    model_to_view_normal = inverse(transpose(Mat3(model_to_view)))
    model_to_clip: Mat4 = (
        view.view_to_clip_transform
        * view.world_to_view_transform
        * model_to_world_transform
    )
    offset_light_position_l = transform_point(
        view.world_to_view_transform,
        # TODO light_position +
        vec3(-1.1, 1.0, 5.0),
    )
    offset_light_position_r = transform_point(
        view.world_to_view_transform,
        # TODO light_position +
        vec3(1.1, 1.0, 5.0),
    )

    gl.glUseProgram(program)

    uniforms = {
        # transforms
        "modelToClipTransform": model_to_clip,
        "modelToViewTransform": model_to_view,
        "modelToViewNormalTransform": model_to_view_normal,
        "viewToWorldRotationTransform": inverse(Mat3(model_to_view)),
        # lighting and color
        "attenuationLinear": 0.07,
        "attenuationQuadratic": 0.017,
        "lightPositionL": offset_light_position_l,
        "lightPositionR": offset_light_position_r,
        "lightColourAndIntensityL": vec3(0.4, 0.4, 0.2),
        "lightColourAndIntensityR": vec3(0.4, 0.4, 0.2),
        "ambientLightColourAndIntensity": vec3(0.05),
        "enableSrgb": True,
        # fog
        "fogExtinctionOffset": 35.0,
        "fogExtinctionCoeff": 0.0015,
        "fogColor": vec3(0.73),
    }

    uniforms.update(uniform_overrides)

    # if verbose is not None:
    # print(list(map(lambda x: str(x)[:5], offset_light_position)), verbose)

    for key, value in uniforms.items():
        set_uniform(program, key, value)
