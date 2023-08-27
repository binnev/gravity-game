from pygame import Rect
from robingame.objects import Entity, Group
from robingame.utils import random_float

from . import utils
from .automaton import GravityAutomatonSparseMatrix, GravityAutomatonDataFrame
from .backend import Backend
from .physics import Body
from .frontend import GravityFrontend, GravityMinimap
from .input_handler import KeyboardHandler
from .viewer import Viewer
from .viewport_handler import DefaultViewportHandler


class GravityScene(Entity):
    def __init__(self):
        super().__init__()

        # automaton = GravityAutomatonSparseMatrix()
        automaton = GravityAutomatonDataFrame()
        # utils.create_solar_system(automaton)
        utils.spawn_line(automaton)
        backend = Backend(automaton=automaton)
        main_rect = Rect(0, 0, 1000, 1000)
        size = max(automaton.world_size())
        viewport_handler = DefaultViewportHandler(
            x=0,
            y=0,
            width=size,
            height=size,
        )
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
