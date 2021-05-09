from entities.ObjModel import ObjModel


class Entity:
    name = None
    filename = None
    model = None

    def __init__(self, name=None, filename=None):
        """
        kwargs:
            name: str
            filename: str
        """
        self.name = name
        self.filename = filename
        self._init_resources()

    def _init_resources(self):
        self.model = ObjModel(self.filename)

    def update(self, keyboard=None, mouse=None, time=None):
        """
        kwargs:
            keyboard: Keyboard
            mouse: Mouse
            time: Time
        """
        pass

    def draw_ui(self):
        pass

    def render(self):
        pass
