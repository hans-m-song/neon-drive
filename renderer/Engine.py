import sys

import glfw
import imgui
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer

import constants
from renderer.control import Keyboard, Mouse, Time
from utils.log import get_logger

logger = get_logger()
imgui.create_context()
io = imgui.get_io()


def get_info(prop):
    return gl.glGetString(prop).decode("utf8")


def init_window():
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
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

    impl = GlfwRenderer(window)

    if constants.DEBUG:
        gl.glEnable(gl.GL_DEBUG_OUTPUT)
        gl.glEnable(gl.GL_DEBUG_OUTPUT_SYNCHRONOUS)

    gl.glDisable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)

    return window, impl


class Engine:
    window = None
    impl = None

    keyboard = None
    mouse = None
    time = None

    resources = []

    def __init__(self):
        if not glfw.init():
            sys.exit(1)

        self.window, self.impl = init_window()

        logger.debug(f"vendor:   {get_info(gl.GL_VENDOR)}")
        logger.debug(f"renderer: {get_info(gl.GL_RENDERER)}")
        logger.debug(f"version:  {get_info(gl.GL_VERSION)}")

        self.keyboard = Keyboard(self.window)
        self.mouse = Mouse(self.window)
        self.time = Time()

        self.init_resources()

    def add_resource(self, resource):
        self.resources.append(resource)
        logger.debug(f"added resource: {resource.name or resource}")

    def run(self):
        while not glfw.window_should_close(self.window):
            self.tick()

        self._cleanup()

    def init_resources(self):
        pass

    def update(self):
        self.keyboard.update()
        self.mouse.update()
        self.time.update()

        io = imgui.get_io()
        if io.want_capture_mouse:
            self.mouse.delta = (0, 0)

        for resource in self.resources:
            resource.update(
                keyboard=self.keyboard, mouse=self.mouse, time=self.time
            )

    def draw_ui(self, width, height):
        for resource in self.resources:
            resource.draw_ui()

    def render(self, width, height):
        for resource in self.resources:
            resource.render()

    def tick(self):
        self.update()

        width, height = glfw.get_framebuffer_size(self.window)

        imgui.new_frame()
        imgui.set_next_window_position(5.0, 5.0, imgui.FIRST_USE_EVER)
        imgui.begin("UI", 0)

        self.draw_ui(width, height)
        self.render(width, height)

        imgui.end()
        imgui.render()
        glfw.swap_buffers(self.window)
        glfw.poll_events()
        self.impl.process_inputs()

    def _cleanup(self):
        glfw.terminate()
