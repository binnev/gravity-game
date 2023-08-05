import pygame.draw
from pygame import Surface, Color, Rect

from .automaton import Automaton
from .transform import Transform
from .viewport_handler import FloatRect


class GravityFrontend:
    def draw(
        self,
        surface: Surface,
        automaton: Automaton,
        viewport: FloatRect,
        debug: bool = False,
    ):
        """
        For now just draw everything
        """
        surface.fill(Color("black"))

        viewport_rect_xy = Rect(*viewport).inflate(2, 2)
        visible = {
            (x, y): body
            for (x, y), body in automaton.bodies().items()
            if viewport_rect_xy.colliderect(
                Rect(x - body.radius, y - body.radius, body.radius * 2, body.radius * 2)
            )
        }

        image_rect_uv = surface.get_rect()
        transform = Transform(viewport, image_rect_uv)

        for xy, body in visible.items():
            color = self.get_color(body)
            uv = transform.point(xy)
            radius = body.radius * transform.scale
            radius = max(1, radius)
            pygame.draw.circle(surface, color, center=uv, radius=radius)

    def get_color(self, body):
        return Color("red")


class GravityMinimap:
    def draw(
        self,
        surface: Surface,
        automaton: Automaton,
        viewport: FloatRect,
        debug: bool = False,
    ):
        """
        For now just draw everything
        """
        surface.fill(Color("black"))

        # Choose viewport in xy coordinates to filter for visible cells
        # fit viewport as tightly as possible to world limits
        world_width, world_height = automaton.world_size()
        (xmin, xmax), (ymin, ymax) = automaton.world_limits()
        world_rect_xy = Rect(xmin, ymin, world_width, world_height)
        image_rect_uv = surface.get_rect()
        transform = Transform(world_rect_xy, image_rect_uv)
        viewport_rect_uv = transform.floatrect(viewport)

        # Draw all cells in screen coords
        for xy, body in automaton.bodies().items():
            color = self.get_color(body)
            uv = transform.point(xy)
            radius = body.radius * transform.scale
            radius = max(radius, 1)
            pygame.draw.circle(surface, color, center=uv, radius=radius)

        pygame.draw.rect(surface, Color("white"), viewport_rect_uv, 1)
        if debug:
            world_rect_uv = transform.rect(world_rect_xy)
            pygame.draw.rect(surface, Color("yellow"), world_rect_uv, 1)

    def get_color(self, value):
        return Color("red")
