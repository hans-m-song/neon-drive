from entities.ObjModel import ObjModel
from renderer.control import Keyboard, Mouse, Time
from renderer.View import View


class Entity:
    name: str
    filename: str
    model: ObjModel
    position = [0.0, 0.0, 0.0]

    def __init__(self, name: str = None, filename: str = None):
        """
        kwargs:
            name: str
            filename: str
        """
        assert name is not None
        assert filename is not None

        self.name = name
        self.filename = filename
        self._init_resources()

    def _init_resources(self):
        self.model = ObjModel(self.filename)

    def update(
        self,
        keyboard: Keyboard = None,
        mouse: Mouse = None,
        time: Time = None,
    ):
        """
        kwargs:
            keyboard: Keyboard
            mouse: Mouse
            time: Time
        """
        assert keyboard is not None
        assert mouse is not None
        assert time is not None

    def draw_ui(self, view: View = None):
        """
        kwargs:
            view: View
        """
        assert view is not None

    def render(self, view: View = None):
        """
        kwargs:
            view: View
        """
        assert view is not None
