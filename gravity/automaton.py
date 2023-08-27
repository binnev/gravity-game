from typing import Protocol

import numpy
from pandas import DataFrame
from robingame.utils import SparseMatrix

from . import physics
from .language import choose_new_name
from .physics import calculate_x_y_acceleration, calculate_distances

CoordFloat2D = tuple[float, float]


class Automaton(Protocol):
    total_mass: float  # calculated every iteration

    def iterate(self):
        ...

    def add_body(
        self,
        x: float,
        y: float,
        mass: float,
        radius: float,
        u: float = 0,
        v: float = 0,
        name: str = "",
    ):
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

        # calculate total mass once per iteration
        self.total_mass = sum(body.mass for body in self.contents.values())

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

    def add_body(
        self,
        x: float,
        y: float,
        mass: float,
        radius: float,
        u: float = 0,
        v: float = 0,
        name: str = "",
    ):
        self.contents[(x, y)] = physics.Body(mass=mass, radius=radius, u=u, v=v, name=name)

    def bodies(self) -> dict[CoordFloat2D, physics.Body]:
        return self.contents

    def world_size(self) -> tuple[float, float]:
        return self.contents.size

    def world_limits(self) -> tuple[tuple[float, float], tuple[float, float]]:
        return self.contents.limits


class GravityAutomatonDataFrame:
    contents: DataFrame

    def __init__(self):
        self.contents = DataFrame(columns="x y mass radius u v name".split())

    def iterate(self):
        """
        1. Apply the rules of gravitation attraction between each pair of objects
        2. Move every object according to the laws of motion
        """

        x = self.contents.x.values
        y = self.contents.y.values
        mass = self.contents.mass.values
        acc_x, acc_y = calculate_x_y_acceleration(x, y, mass)

        # update velocities
        self.contents.u += acc_x
        self.contents.v += acc_y
        # update positions
        self.contents.x += self.contents.u
        self.contents.y += self.contents.v

        # do collisions
        while self.do_collisions():
            pass

        # calculate total mass once per iteration
        self.total_mass = self.contents.mass.sum()

    def do_collisions(self) -> bool:
        """
        fixme: refactor
        Do one round of collision processing.
        Return True if collisions were processed.
        """
        DX, DY, DIST = calculate_distances(self.contents.x.values, self.contents.y.values)
        radii = self.contents.radius.values
        R1R2 = radii.reshape(-1, 1) + radii.reshape(1, -1)
        ZERO_DIAGONAL = numpy.ones_like(R1R2) - numpy.eye(len(R1R2))
        R1R2 = R1R2 * ZERO_DIAGONAL
        colliding = DIST < R1R2
        iis, jjs = colliding.nonzero()
        for i, j in zip(iis, jjs):
            m_i = self.contents.mass[i]
            m_j = self.contents.mass[j]
            x_i = self.contents.x[i]
            x_j = self.contents.x[j]
            y_i = self.contents.y[i]
            y_j = self.contents.y[j]
            u_i = self.contents.u[i]
            u_j = self.contents.u[j]
            v_i = self.contents.v[i]
            v_j = self.contents.v[j]
            r_i = self.contents.radius[i]
            r_j = self.contents.radius[j]
            name_i = self.contents.name[i]
            name_j = self.contents.name[j]
            new_x = (x_i * m_i + x_j * m_j) / (m_i + m_j)
            new_y = (y_i * m_i + y_j * m_j) / (m_i + m_j)
            new_u = (m_i * u_i + m_j * u_j) / (m_i + m_j)
            new_v = (m_i * v_i + m_j * v_j) / (m_i + m_j)
            new_radius = numpy.sqrt(r_i**2 + r_j**2)
            new_name = choose_new_name(name_i, name_j, m_i, m_j)
            self.contents.drop(i, inplace=True)
            self.contents.drop(j, inplace=True)
            self.add_body(
                x=new_x,
                y=new_y,
                mass=m_i + m_j,
                radius=new_radius,
                u=new_u,
                v=new_v,
                name=new_name,
            )
            return True

        return False

    def add_body(
        self,
        x: float,
        y: float,
        mass: float,
        radius: float,
        u: float = 0,
        v: float = 0,
        name: str = "",
    ):
        """
        Add a body to the automaton. This makes a full copy of the contents dataframe,
        so it's quite slow. Use sparingly.
        """
        self.contents = DataFrame(
            [
                *self.contents.to_dict(orient="records"),
                dict(x=x, y=y, mass=mass, radius=radius, u=u, v=v, name=name),
            ]
        )

    def bodies(self) -> dict[CoordFloat2D, physics.Body]:
        return {
            (body.x, body.y): physics.Body(
                mass=body.mass,
                radius=body.radius,
                u=body.u,
                v=body.v,
                name=body["name"],  # .name is reserved; it's the name of the series.
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
