import sys

import glfw

import OpenGL.GL as gl

import constants
from renderer.control import Keyboard, Mouse, Time
from renderer.View import View
from utils.log import get_logger
from time import sleep


logger = get_logger()


def get_info(prop):
    return gl.glGetString(prop).decode("utf8")


def init_window():
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SRGB_CAPABLE, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(
        constants.WINDOW_WIDTH,
        constants.WINDOW_HEIGHT,
        constants.WINDOW_NAME,
        None,
        None,
    )

    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)

    if constants.CAPTURE_MOUSE:
        glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    gl.glDisable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)

    return window


class Engine:
    window = None

    time: Time = None
    keyboard: Keyboard = None
    mouse: Mouse = None
    view: View = None

    s_per_frame = 1.0 / constants.TARGET_FPS

    resources = []

    def __init__(self):
        if not glfw.init():
            sys.exit(1)

        self.window = init_window()

        logger.info(f"vendor:   {get_info(gl.GL_VENDOR)}")
        logger.info(f"renderer: {get_info(gl.GL_RENDERER)}")
        logger.info(f"version:  {get_info(gl.GL_VERSION)}")

        self.keyboard = Keyboard(self.window)
        self.mouse = Mouse(self.window)
        self.time = Time()
        self.view = View(mouse=self.mouse)

        self.init_resources()

    def add_resource(self, resource):
        self.resources.append(resource)
        logger.debug(f"added resource: {resource}")

    def run(self):
        while not glfw.window_should_close(self.window):
            self.tick()

        self._cleanup()

    def init_resources(self):
        pass

    def update(self, width, height):
        self.time.update()
        self.keyboard.update()
        self.mouse.update()
        self.view.update(width, height)

        for resource in self.resources:
            resource.update(
                keyboard=self.keyboard,
                mouse=self.mouse,
                time=self.time,
            )

    def render(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glClearColor(0.2, 0.3, 0.1, 1.0)
        gl.glClear(gl.GL_DEPTH_BUFFER_BIT | gl.GL_COLOR_BUFFER_BIT)

        for resource in self.resources:
            resource.render(view=self.view)

    def tick(self):
        width, height = glfw.get_framebuffer_size(self.window)

        self.update(width, height)
        self.render(width, height)

        glfw.swap_buffers(self.window)
        glfw.poll_events()

        # ensure movement speed scaling is right
        leftover = self.s_per_frame - self.time.delta
        if leftover > 0:
            sleep(leftover)

    def _cleanup(self):
        glfw.terminate()
