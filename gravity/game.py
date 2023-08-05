from pygame import Color
from robingame.objects import Game, Group

from gravity.scene import GravityScene


class GravityGame(Game):
    fps = 64
    window_width = 1000
    window_height = 1000
    window_caption = "Gravity"
    screen_color = Color("black")

    def __init__(self):
        super().__init__()
        self.scenes = Group()
        self.child_groups = [self.scenes]
        self.scenes.add(GravityScene())


if __name__ == "__main__":
    GravityGame().main()
