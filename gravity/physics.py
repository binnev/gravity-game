import numpy
import math
from dataclasses import dataclass

from . import constants
from .constants import GRAVITATIONAL_CONSTANT
from .vector import Vector2D


@dataclass
class Body:
    mass: float  # kg
    radius: float  # m
    u: float = 0  # m/s
    v: float = 0  # m/s


def euclidian_distance(xy1, xy2) -> float:
    """
    Calculate the Euclidian distance between two objects
    """
    x1, y1 = xy1
    x2, y2 = xy2
    delta_x = abs(x2 - x1)
    delta_y = abs(y2 - y1)
    return math.sqrt(delta_x**2 + delta_y**2)


def attraction_force(xy1, xy2, mass1: float, mass2: float) -> float:
    """
    Calculate the force of attraction between two bodies according to Newton's law of
    gravitation:
        F = G * (m1 * m2) / R**2
    """
    distance = euclidian_distance(xy1, xy2)
    return constants.GRAVITATIONAL_CONSTANT * (mass1 * mass2) / distance**2


def newtonian_acceleration(body: Body, force: float) -> float:
    """
    Calculate the acceleration on a body caused by a force, according to Newton's second law of
    motion:
        F = m * a
    or
        a = F / m
    """
    return force / body.mass


def gravitational_attraction(body1: Body, xy1, body2: Body, xy2):
    """
    1. Calculate the gravitational attraction force between two objects
    2. Calculate the resulting acceleration for each object based on its mass
    3. Calculate the x/y components of the acceleration for each object
    4. Adjust each objects u/v according to its acceleration
    """

    # 1
    force = attraction_force(xy1, xy2, body1.mass, body2.mass)
    # 2
    acc1 = newtonian_acceleration(body1, force)
    acc2 = newtonian_acceleration(body2, force)
    # 3
    x1, y1 = xy1
    x2, y2 = xy2
    dx = x2 - x1
    dy = y2 - y1
    vector = Vector2D(dx, dy)  # vector from body1 to body2
    unit = vector.unit()
    acc1_x = acc1 * unit.dx
    acc1_y = acc1 * unit.dy
    vector = vector.reverse()
    unit = vector.unit()
    acc2_x = acc2 * unit.dx
    acc2_y = acc2 * unit.dy

    # 4
    body1.u += acc1_x
    body1.v += acc1_y
    body2.u += acc2_x
    body2.v += acc2_y


# ================== matrix algebra solution =========================
def calculate_distances(
    x: numpy.array, y: numpy.array
) -> tuple[numpy.array, numpy.array, numpy.ndarray]:
    X = x.reshape(-1, 1)
    Y = y.reshape(-1, 1)
    ones = numpy.ones_like(X).T
    X1 = X.dot(ones)
    X2 = X1.T
    Y1 = Y.dot(ones)
    Y2 = Y1.T
    DX = X2 - X1
    DY = Y2 - Y1
    DIST = numpy.sqrt(DX**2 + DY**2)
    return DX, DY, DIST


def calculate_attraction_forces(mass: numpy.array, DIST: numpy.ndarray) -> numpy.ndarray:
    """
    Calculate attraction force by F = G * (m1 * m2) / R**2

    :param mass: 1d array of masses
    :param DIST: 2d array of distances where DIST[i, j] is the distance from body i to body j
    :return: 2d array of attraction forces where FORCE[i, j] is the force on body i due to body j
    """
    MASS = mass.reshape(1, -1)
    M1M2 = MASS.T.dot(MASS)
    DIST[DIST == 0] = 1  # avoid division by zero
    ZERO_DIAGONAL = numpy.ones_like(M1M2) - numpy.eye(len(M1M2))
    M1M2 = M1M2 * ZERO_DIAGONAL
    FORCE = GRAVITATIONAL_CONSTANT * M1M2 / DIST**2
    return FORCE


def calculate_accelerations(FORCE: numpy.ndarray, mass: numpy.array) -> numpy.ndarray:
    """
    Calculate acceleration by a = F / m

    :param FORCE: 2d array of attraction forces where FORCE[i, j] is the force on
        body i due to body j
    :param mass: 1d array of masses
    :return: 2d array of accelerations where ACCELERATION[i, j] is the acceleration
        of body i due to body j
    """

    MASS = mass.reshape(-1, 1)
    ONES = numpy.ones_like(MASS.T)
    MASS_ARRAY = MASS.dot(ONES)
    ACCELERATION = FORCE / MASS_ARRAY
    return ACCELERATION


def calculate_x_y_acceleration(
    x: numpy.array,
    y: numpy.array,
    mass: numpy.array,
) -> tuple[numpy.array, numpy.array]:
    """
    Given the x/y coordinates and masses of a set of bodies, calculate the x/y acceleration of
    the bodies due to gravitational attraction.
    :param x: 1d array of x coordinates
    :param y: 1d array of y coordinates
    :param mass: 1d array of masses
    :return acc_x: 1d array of x accelerations
    :return acc_y: 1d array of y accelerations
    """
    DX, DY, DIST = calculate_distances(x, y)
    FORCE = calculate_attraction_forces(mass, DIST)
    ACCELERATION = calculate_accelerations(FORCE, mass)
    UNIT_X = DX / DIST
    UNIT_Y = DY / DIST
    ACC_X = ACCELERATION * UNIT_X
    ACC_Y = ACCELERATION * UNIT_Y
    acc_x = ACC_X.sum(axis=1)
    acc_y = ACC_Y.sum(axis=1)
    return acc_x, acc_y
