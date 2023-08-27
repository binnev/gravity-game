import matplotlib
import pygame.draw
from pygame import Surface, Color
from robingame.text import fonts

from .automaton import Automaton
from .physics import Body
from .transform import Transform
from .utils import overlap, square_text
from .viewport_handler import FloatRect


class GravityFrontend:
    colormap = matplotlib.cm.cividis

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

        visible = {
            (x, y): body
            for (x, y), body in automaton.bodies().items()
            if (
                overlap(
                    (x - body.radius, x + body.radius), (viewport[0], viewport[0] + viewport[2])
                )
                and overlap(
                    (y - body.radius, y + body.radius), (viewport[1], viewport[1] + viewport[3])
                )
            )
        }

        image_rect_uv = surface.get_rect()
        transform = Transform(viewport, image_rect_uv)

        for xy, body in visible.items():
            color = self.get_color(body, automaton)
            uv = transform.point(xy)
            radius = body.radius * transform.scale
            radius = max(2, radius)
            pygame.draw.circle(surface, color, center=uv, radius=radius)
            if body.name:
                fonts.cellphone_white.render(
                    surface,
                    square_text(body.name),
                    x=uv[0],
                    y=uv[1],
                    scale=2,
                )

    def get_color(self, body: Body, automaton: Automaton) -> Color:
        """
        Linearly interpolate a body's mass onto a colour scale,
        where MIN maps to the lower limit of the colormap,
        and MAX maps to the upper limit.
        """
        MIN_BRIGHTNESS = 0.2
        interpolated = body.mass / automaton.total_mass
        interpolated = max(interpolated, MIN_BRIGHTNESS)
        return Color(*tuple(int(ch * 255) for ch in self.colormap(interpolated)))


class GravityMinimap(GravityFrontend):
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
        world_rect_xy = FloatRect((xmin, ymin, world_width, world_height))
        image_rect_uv = surface.get_rect()
        transform = Transform(world_rect_xy, image_rect_uv)
        viewport_rect_uv = transform.floatrect(viewport)

        # Draw all cells in screen coords
        for xy, body in automaton.bodies().items():
            color = self.get_color(body, automaton)
            uv = transform.point(xy)
            radius = body.radius * transform.scale
            radius = max(radius, 2)
            pygame.draw.circle(surface, color, center=uv, radius=radius)

        pygame.draw.rect(surface, Color("white"), viewport_rect_uv, 1)
        if debug:
            world_rect_uv = transform.rect(world_rect_xy)
            pygame.draw.rect(surface, Color("yellow"), world_rect_uv, 1)
