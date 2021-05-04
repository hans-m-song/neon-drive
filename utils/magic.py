import sys

# we use 'warnings' to remove this warning that ImGui[glfw] gives
import warnings

import glfw
import imgui
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer as ImGuiGlfwRenderer

import constants

imgui.create_context()
warnings.simplefilter(action="ignore", category=FutureWarning)
g_mousePos = [0.0, 0.0]


def debugMessageCallback(
    source, type, id, severity, length, message, userParam
):
    print(message)


def initGlFwAndResources(title, startWidth, startHeight, initResources):
    global g_mousePos

    # glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, 1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.SRGB_CAPABLE, 1)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # glfw.window_hint(glfw.SAMPLES, g_currentMsaaSamples)

    window = glfw.create_window(startWidth, startHeight, title, None, None)
    if not window:
        glfw.terminate()
        sys.exit(1)

    glfw.make_context_current(window)

    print(
        "--------------------------------------\nOpenGL\n  "
        + "Vendor: {}\n  Renderer: {}\n  Version: {}".format(
            gl.glGetString(gl.GL_VENDOR).decode("utf8"),
            gl.glGetString(gl.GL_RENDERER).decode("utf8"),
            gl.glGetString(gl.GL_VERSION).decode("utf8"),
        )
        + "\n--------------------------------------\n",
        flush=True,
    )

    impl = ImGuiGlfwRenderer(window)

    # gl.glDebugMessageCallback(gl.GLDEBUGPROC(debugMessageCallback), None)

    if constants.DEBUG:
        # (although this gl.glEnable(gl.GL_DEBUG_OUTPUT) should not have been
        # needed when using the gl.GLUT_DEBUG flag above...)
        gl.glEnable(gl.GL_DEBUG_OUTPUT)
        # This ensures that the callback is done in the context of the calling
        # function, which means it will be on the stack in the debugger, which
        # makes it a lot easier to figure out why it happened.
        gl.glEnable(gl.GL_DEBUG_OUTPUT_SYNCHRONOUS)

    gl.glDisable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LEQUAL)
    # gl.glEnable(gl.GL_DEPTH_CLAMP)

    if initResources:
        initResources()

    return window, impl


# add anything here that must be deleted when creating a new context
def cleaupGlResources():
    pass


def runProgram(
    title,
    startWidth,
    startHeight,
    renderFrame,
    initResources=None,
    drawUi=None,
    update=None,
):
    global g_mousePos

    if not glfw.init():
        sys.exit(1)

    window, impl = initGlFwAndResources(
        title, startWidth, startHeight, initResources
    )

    currentTime = glfw.get_time()
    prevMouseX, prevMouseY = glfw.get_cursor_pos(window)

    while not glfw.window_should_close(window):
        prevTime = currentTime
        currentTime = glfw.get_time()
        dt = currentTime - prevTime

        keyStateMap = {}
        for name, id in g_glfwKeymap.items():
            keyStateMap[name] = glfw.get_key(window, id) == glfw.PRESS

        for name, id in g_glfwMouseMap.items():
            keyStateMap[name] = glfw.get_mouse_button(window, id) == glfw.PRESS

        mouseX, mouseY = glfw.get_cursor_pos(window)
        g_mousePos = [mouseX, mouseY]

        # Udpate 'game logic'
        if update:
            imIo = imgui.get_io()
            mouseDelta = [mouseX - prevMouseX, mouseY - prevMouseY]
            if imIo.want_capture_mouse:
                mouseDelta = [0, 0]
            update(dt, keyStateMap, mouseDelta)
        prevMouseX, prevMouseY = mouseX, mouseY

        width, height = glfw.get_framebuffer_size(window)

        imgui.new_frame()

        imgui.set_next_window_position(5.0, 5.0, imgui.FIRST_USE_EVER)
        # imgui.set_next_window_size(400.0, 620.0, imgui.FIRST_USE_EVER)
        imgui.begin("UI", 0)

        if drawUi:
            drawUi(width, height)

        renderFrame(width, height)

        # mgui.show_test_window()

        imgui.end()

        imgui.render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()
        impl.process_inputs()

    glfw.terminate()


def getUniformLocationDebug(shaderProgram, name):
    loc = gl.glGetUniformLocation(shaderProgram, name)
    # Useful point for debugging, replace with silencable logging
    # if loc == -1:
    #    print("Uniforn '%s' was not found"%name)
    return loc


g_glfwMouseMap = {
    "MOUSE_BUTTON_LEFT": glfw.MOUSE_BUTTON_LEFT,
    "MOUSE_BUTTON_RIGHT": glfw.MOUSE_BUTTON_RIGHT,
    "MOUSE_BUTTON_MIDDLE": glfw.MOUSE_BUTTON_MIDDLE,
}


g_glfwKeymap = {
    "SPACE": glfw.KEY_SPACE,
    "APOSTROPHE": glfw.KEY_APOSTROPHE,
    "COMMA": glfw.KEY_COMMA,
    "MINUS": glfw.KEY_MINUS,
    "PERIOD": glfw.KEY_PERIOD,
    "SLASH": glfw.KEY_SLASH,
    "0": glfw.KEY_0,
    "1": glfw.KEY_1,
    "2": glfw.KEY_2,
    "3": glfw.KEY_3,
    "4": glfw.KEY_4,
    "5": glfw.KEY_5,
    "6": glfw.KEY_6,
    "7": glfw.KEY_7,
    "8": glfw.KEY_8,
    "9": glfw.KEY_9,
    "SEMICOLON": glfw.KEY_SEMICOLON,
    "EQUAL": glfw.KEY_EQUAL,
    "A": glfw.KEY_A,
    "B": glfw.KEY_B,
    "C": glfw.KEY_C,
    "D": glfw.KEY_D,
    "E": glfw.KEY_E,
    "F": glfw.KEY_F,
    "G": glfw.KEY_G,
    "H": glfw.KEY_H,
    "I": glfw.KEY_I,
    "J": glfw.KEY_J,
    "K": glfw.KEY_K,
    "L": glfw.KEY_L,
    "M": glfw.KEY_M,
    "N": glfw.KEY_N,
    "O": glfw.KEY_O,
    "P": glfw.KEY_P,
    "Q": glfw.KEY_Q,
    "R": glfw.KEY_R,
    "S": glfw.KEY_S,
    "T": glfw.KEY_T,
    "U": glfw.KEY_U,
    "V": glfw.KEY_V,
    "W": glfw.KEY_W,
    "X": glfw.KEY_X,
    "Y": glfw.KEY_Y,
    "Z": glfw.KEY_Z,
    "LEFT_BRACKET": glfw.KEY_LEFT_BRACKET,
    "BACKSLASH": glfw.KEY_BACKSLASH,
    "RIGHT_BRACKET": glfw.KEY_RIGHT_BRACKET,
    "GRAVE_ACCENT": glfw.KEY_GRAVE_ACCENT,
    "WORLD_1": glfw.KEY_WORLD_1,
    "WORLD_2": glfw.KEY_WORLD_2,
    "ESCAPE": glfw.KEY_ESCAPE,
    "ENTER": glfw.KEY_ENTER,
    "TAB": glfw.KEY_TAB,
    "BACKSPACE": glfw.KEY_BACKSPACE,
    "INSERT": glfw.KEY_INSERT,
    "DELETE": glfw.KEY_DELETE,
    "RIGHT": glfw.KEY_RIGHT,
    "LEFT": glfw.KEY_LEFT,
    "DOWN": glfw.KEY_DOWN,
    "UP": glfw.KEY_UP,
    "PAGE_UP": glfw.KEY_PAGE_UP,
    "PAGE_DOWN": glfw.KEY_PAGE_DOWN,
    "HOME": glfw.KEY_HOME,
    "END": glfw.KEY_END,
    "CAPS_LOCK": glfw.KEY_CAPS_LOCK,
    "SCROLL_LOCK": glfw.KEY_SCROLL_LOCK,
    "NUM_LOCK": glfw.KEY_NUM_LOCK,
    "PRINT_SCREEN": glfw.KEY_PRINT_SCREEN,
    "PAUSE": glfw.KEY_PAUSE,
    "F1": glfw.KEY_F1,
    "F2": glfw.KEY_F2,
    "F3": glfw.KEY_F3,
    "F4": glfw.KEY_F4,
    "F5": glfw.KEY_F5,
    "F6": glfw.KEY_F6,
    "F7": glfw.KEY_F7,
    "F8": glfw.KEY_F8,
    "F9": glfw.KEY_F9,
    "F10": glfw.KEY_F10,
    "F11": glfw.KEY_F11,
    "F12": glfw.KEY_F12,
    "F13": glfw.KEY_F13,
    "F14": glfw.KEY_F14,
    "F15": glfw.KEY_F15,
    "F16": glfw.KEY_F16,
    "F17": glfw.KEY_F17,
    "F18": glfw.KEY_F18,
    "F19": glfw.KEY_F19,
    "F20": glfw.KEY_F20,
    "F21": glfw.KEY_F21,
    "F22": glfw.KEY_F22,
    "F23": glfw.KEY_F23,
    "F24": glfw.KEY_F24,
    "F25": glfw.KEY_F25,
    "KP_0": glfw.KEY_KP_0,
    "KP_1": glfw.KEY_KP_1,
    "KP_2": glfw.KEY_KP_2,
    "KP_3": glfw.KEY_KP_3,
    "KP_4": glfw.KEY_KP_4,
    "KP_5": glfw.KEY_KP_5,
    "KP_6": glfw.KEY_KP_6,
    "KP_7": glfw.KEY_KP_7,
    "KP_8": glfw.KEY_KP_8,
    "KP_9": glfw.KEY_KP_9,
    "KP_DECIMAL": glfw.KEY_KP_DECIMAL,
    "KP_DIVIDE": glfw.KEY_KP_DIVIDE,
    "KP_MULTIPLY": glfw.KEY_KP_MULTIPLY,
    "KP_SUBTRACT": glfw.KEY_KP_SUBTRACT,
    "KP_ADD": glfw.KEY_KP_ADD,
    "KP_ENTER": glfw.KEY_KP_ENTER,
    "KP_EQUAL": glfw.KEY_KP_EQUAL,
    "LEFT_SHIFT": glfw.KEY_LEFT_SHIFT,
    "LEFT_CONTROL": glfw.KEY_LEFT_CONTROL,
    "LEFT_ALT": glfw.KEY_LEFT_ALT,
    "LEFT_SUPER": glfw.KEY_LEFT_SUPER,
    "RIGHT_SHIFT": glfw.KEY_RIGHT_SHIFT,
    "RIGHT_CONTROL": glfw.KEY_RIGHT_CONTROL,
    "RIGHT_ALT": glfw.KEY_RIGHT_ALT,
    "RIGHT_SUPER": glfw.KEY_RIGHT_SUPER,
    "MENU": glfw.KEY_MENU,
}
