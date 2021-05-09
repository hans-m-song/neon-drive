import glfw

from utils.magic import g_glfwKeymap, g_glfwMouseMap


class WithWindow:
    def __init__(self, window):
        self.window = window


class Keyboard(WithWindow):
    state = {}

    def update(self):
        state = {}
        for name, id in g_glfwKeymap.items():
            state[name] = glfw.get_key(self.window, id) == glfw.PRESS

        for name, id in g_glfwMouseMap.items():
            state[name] = glfw.get_mouse_button(self.window, id) == glfw.PRESS

        self.state = {}


class Mouse(WithWindow):
    position = (0, 0)
    delta = (0, 0)

    def update(self):
        old_x, old_y = self.position
        x, y = glfw.get_cursor_pos(self.window)

        self.delta = (x - old_x, y - old_y)
        self.position = (x, y)


class Time:
    now = glfw.get_time()
    delta = 0

    def update(self):
        prev_time = self.now
        self.now = glfw.get_time()
        self.delta = self.now - prev_time
