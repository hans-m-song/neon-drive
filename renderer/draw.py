import OpenGL.GL as gl

from entities.Entity import Entity
from renderer.View import View
from utils.math import Mat3, Mat4, inverse, transpose


def draw_obj(
    model: Entity = None,
    view: View = None,
    model_to_world: Mat4 = None,
):
    assert model is not None
    assert view is not None
    assert model_to_world is not None

    model_to_view = view.world_to_view_transform * model_to_world
    model_to_view_normal = inverse(transpose(Mat3(model_to_view)))

    gl.glUseProgram(model.defaultShader)

    view_light_space_direction = [0.0, 0.0, -1.0]
    gl.glUniform3fv(
        gl.glGetUniformLocation(
            model.defaultShader,
            "viewSpaceLightDirection",
        ),
        1,
        view_light_space_direction,
    )

    transforms = {
        "modelToClipTransform": view.view_to_clip_transform
        * view.world_to_view_transform
        * model_to_world,
        "modelToViewTransform": model_to_view,
        "modelToViewNormalTransform": model_to_view_normal,
    }

    model.render(None, None, transforms)
