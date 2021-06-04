from typing import Callable, Tuple

import OpenGL.GL as gl
from numpy import void
from PIL import Image

from shader.utils import set_uniform
from utils.log import get_logger

logger = get_logger()


class Texture:
    texture_id: int
    size: Tuple[float, float]

    def __init__(
        self,
        filename: str,
        set_parameters: Callable[[], None] = lambda _: None,
        mode="RGB",
    ) -> None:
        self.texture_id = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.texture_id)

        with Image.open(f"assets/{filename}") as image:
            self.size = image.size
            data = image.tobytes("raw", mode, 0, -1)

            gl.glTexImage2D(
                gl.GL_TEXTURE_2D,
                0,
                gl.GL_RGBA,
                *self.size,
                0,
                gl.GL_RGBA,
                gl.GL_UNSIGNED_BYTE,
                data,
            )

            gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

            set_parameters()

            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        logger.debug(f"loaded texture: (id {self.texture_id}) {filename}")

    def use(self):
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(
            gl.GL_TEXTURE_2D,
            self.texture_id,
        )
