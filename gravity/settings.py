from dataclasses import dataclass

import pygame
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class KeyBinds:
    pause: int = pygame.K_SPACE
    up: int = pygame.K_w
    down: int = pygame.K_s
    left: int = pygame.K_a
    right: int = pygame.K_d
    zoom_in: int = pygame.K_e
    zoom_out: int = pygame.K_q
    something: int = pygame.K_RIGHT
