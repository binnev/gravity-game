import pygame.display
from pygame import Surface
from robingame.animation import ease_out, ease_in
from robingame.gui import Menu
from robingame.objects import Group, Entity
from typing import Callable

from robingame.text import fonts

from gravity.settings import KeyBinds


class PauseMenu(Menu):
    def __init__(self):
        super().__init__()
        self.entities = Group()
        self.child_groups += [self.entities]
        self.entities.add(Toast("Paused", y=10))
        self.entities.add(Toast("Controls:", y=100, from_above=False))
        keybinds = KeyBinds()
        yy = 20
        for action, key in keybinds.to_dict().items():
            self.entities.add(Toast(f"Press {key} to {action}", y=100 + yy, from_above=False))
            yy += 20


class FlyingGuiMixin(Entity):
    start_x: int
    start_y: int
    target_x: int
    target_y: int
    state_idle: Callable
    animation_duration: int = 15

    def __init__(self):
        super().__init__()
        self.state = self.state_animate_in

    def state_animate_in(self):
        self.y = ease_out(
            x=self.tick,
            start=self.start_y,
            stop=self.target_y,
            num=self.animation_duration,
        )
        if self.tick == self.animation_duration - 1:
            self.state = self.state_idle

    def state_animate_out(self):
        self.y = ease_in(
            x=self.tick,
            start=self.target_y,
            stop=self.start_y,
            num=self.animation_duration,
        )
        if self.tick == self.animation_duration - 1:
            self.kill()

    def state_idle(self):
        pass

    def exit(self):
        self.state = self.state_animate_out


class Toast(FlyingGuiMixin):
    def __init__(self, text, y=10, from_above=True, font=fonts.cellphone_white, **font_params):
        super().__init__()
        _, height = pygame.display.get_window_size()
        self.from_above = from_above
        self.target_y = y
        self.start_y = -35 if from_above else height + 20
        self.text = text
        self.font = font
        self.font_params = font_params

    def draw(self, surface: Surface, debug: bool = False):
        width, _ = pygame.display.get_window_size()
        params = dict(wrap=width, align=-1, scale=2)
        params.update(self.font_params)
        self.font.render(surface, text=self.text, x=0, y=self.y, **params)
