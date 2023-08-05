from pygame import Rect
from robingame.objects import Entity, Group
from robingame.utils import random_float

from .automaton import GravityAutomaton
from .backend import Backend
from .body import Body
from .frontend import GravityFrontend, GravityMinimap
from .input_handler import KeyboardHandler
from .viewer import Viewer
from .viewport_handler import DefaultViewportHandler


class GravityScene(Entity):
    def __init__(self):
        super().__init__()

        automaton = GravityAutomaton()
        for _ in range(200):
            x = random_float(-500, 500)
            y = random_float(-500, 500)
            u = random_float(-2, 2)
            v = random_float(-2, 2)
            radius = random_float(1, 10)
            mass = radius * 9999999999
            automaton.add_body(x, y, body=Body(radius=radius, mass=mass, u=u, v=v))

        backend = Backend(automaton=automaton)
        main_rect = Rect(0, 0, 1000, 1000)
        viewport_handler = DefaultViewportHandler(
            x=0,
            y=0,
            width=main_rect.width,
            height=main_rect.height,
        )
        viewport_handler.MAX_WIDTH = viewport_handler.MAX_HEIGHT = 10000
        main_map = Viewer(
            rect=main_rect,
            backend=backend,
            frontend=GravityFrontend(),
            controller=KeyboardHandler(),
            viewport_handler=viewport_handler,
        )
        mini_rect = Rect(0, 0, 200, 200)
        mini_rect.topright = (main_rect.right - 10, main_rect.top + 100)
        mini_map = Viewer(
            rect=mini_rect,
            backend=backend,
            frontend=GravityMinimap(),
            viewport_handler=main_map.viewport_handler,
        )

        self.children = Group()
        self.child_groups += [self.children]
        self.children.add(
            backend,
            main_map,
            mini_map,
        )
