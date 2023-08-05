from typing import Protocol

import numpy
from pandas import DataFrame
from robingame.utils import SparseMatrix

from . import physics

CoordFloat2D = tuple[float, float]


class Automaton(Protocol):
    def iterate(self):
        ...

    def add_body(self, x: float, y: float, mass: float, radius: float, u: float = 0, v: float = 0):
        ...

    def bodies(self) -> dict[CoordFloat2D, physics.Body]:
        ...

    def world_size(self) -> tuple[float, float]:
        ...

    def world_limits(self) -> tuple[tuple[float, float], tuple[float, float]]:
        ...


class GravityAutomatonSparseMatrix:
    contents: SparseMatrix[CoordFloat2D, physics.Body]

    def __init__(self):
        self.contents = SparseMatrix()

    def iterate(self):
        """
        1. Apply the rules of gravitation attraction between each pair of objects
        2. Move every object according to the laws of motion
        """
        # 1
        for xy1, body1 in self.contents.items():
            for xy2, body2 in self.contents.items():
                if body1 is body2:
                    continue  # bodies can't affect themselves
                physics.gravitational_attraction(body1, xy1, body2, xy2)

        # 2
        new = SparseMatrix()
        for (x, y), body in self.contents.items():
            x += body.u
            y += body.v
            new[(x, y)] = body
        self.contents = new

        # 3 collisions
        while self.do_collisions():
            pass

    def do_collisions(self) -> bool:
        """
        fixme: refactor
        Do one round of collision processing.
        Return True if collisions were processed.
        """
        for xy1, body1 in self.contents.items():
            for xy2, body2 in self.contents.items():
                if body1 is body2:
                    continue  # bodies can't affect themselves

                dist = physics.euclidian_distance(xy1, xy2)
                if dist < body1.radius + body2.radius:
                    m1, m2 = body1.mass, body2.mass
                    x1, y1 = xy1
                    x2, y2 = xy2
                    new_x = (x1 * m1 + x2 * m2) / (m1 + m2)
                    new_y = (y1 * m1 + y2 * m2) / (m1 + m2)
                    new_u = (m1 * body1.u + m2 * body2.u) / (m1 + m2)
                    new_v = (m1 * body1.v + m2 * body2.v) / (m1 + m2)
                    new_radius = numpy.sqrt(body1.radius**2 + body2.radius**2)
                    new_body = physics.Body(
                        mass=body1.mass + body2.mass,
                        radius=new_radius,
                        u=new_u,
                        v=new_v,
                    )
                    self.contents.pop((x1, y1))
                    self.contents.pop((x2, y2))
                    self.contents[(new_x, new_y)] = new_body
                    return True
        return False

    def add_body(self, x: float, y: float, mass: float, radius: float, u: float = 0, v: float = 0):
        self.contents[(x, y)] = physics.Body(mass=mass, radius=radius, u=u, v=v)

    def bodies(self) -> dict[CoordFloat2D, physics.Body]:
        return self.contents

    def world_size(self) -> tuple[float, float]:
        return self.contents.size

    def world_limits(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return self.contents.limits


class GravityAutomatonDataFrame:
    contents: DataFrame

    def __init__(self):
        self.contents = DataFrame(columns="x y mass radius u v".split())

    def iterate(self):
        """
        1. Apply the rules of gravitation attraction between each pair of objects
        2. Move every object according to the laws of motion
        """
        # 1
        ...

    def do_collisions(self) -> bool:
        """
        fixme: refactor
        Do one round of collision processing.
        Return True if collisions were processed.
        """
        ...

    def add_body(self, x: float, y: float, mass: float, radius: float, u: float = 0, v: float = 0):
        """
        Add a body to the automaton. This makes a full copy of the contents dataframe,
        so it's quite slow. Use sparingly.
        """
        self.contents = DataFrame(
            [
                *self.contents.to_dict(orient="records"),
                dict(x=x, y=y, mass=mass, radius=radius, u=u, v=v),
            ]
        )

    def bodies(self) -> dict[CoordFloat2D, physics.Body]:
        return {
            (body.x, body.y): physics.Body(
                mass=body.mass,
                radius=body.radius,
                u=body.u,
                v=body.v,
            )
            for ii, body in self.contents.iterrows()
        }

    def world_size(self) -> tuple[float, float]:
        xlim, ylim = self.world_limits()
        width = xlim[1] - xlim[0] + 1
        height = ylim[1] - ylim[0] + 1
        return width, height

    def world_limits(self) -> tuple[tuple[float, float], tuple[float, float]]:
        if self.contents.empty:
            return (0, 0), (0, 0)
        else:
            xlim = self.contents.x.min(), self.contents.x.max()
            ylim = self.contents.y.min(), self.contents.y.max()
            return xlim, ylim
