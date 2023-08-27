import math

import numpy
from robingame.utils import random_float

from gravity.automaton import Automaton
from gravity.language import generate_syllable


def create_solar_system(automaton: Automaton):
    """
    Add the bodies in our solar system
    """
    names = ["MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
    masses_e24 = [0.330, 4.87, 5.97, 0.642, 1898, 568, 86.8, 102, 0.013, 0]
    diameters_e3 = [4879, 12104, 12756, 6792, 142984, 120536, 51118, 49528, 2376]
    sun_dist_km_e6 = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0, 5906.4]
    velocities_km_s = [47.4, 35.0, 29.8, 24.1, 13.1, 9.7, 6.8, 5.4, 4.7]
    automaton.add_body(
        x=0,
        y=0,
        mass=1989100000e21,
        radius=695508000,
        name="Sun",
    )  # sun
    for mass, diameter, dist, vel, name in zip(
        masses_e24, diameters_e3, sun_dist_km_e6, velocities_km_s, names
    ):
        mass *= 1e24
        diameter *= 1e3
        dist *= 1e9
        vel *= 1e3
        automaton.add_body(x=0, y=dist, mass=mass, radius=diameter / 2, u=vel, name=name.title())


def spawn_random(automaton: Automaton, n: int = 500):
    for _ in range(500):
        x = random_float(-500, 500)
        y = random_float(-500, 500)
        u = random_float(-2, 2)
        v = random_float(-2, 2)
        radius = random_float(1, 10)
        mass = radius * 9999999999
        name = generate_syllable()
        automaton.add_body(x, y, radius=radius, mass=mass, u=u, v=v, name=name)


def spawn_swirling(automaton: Automaton, n: int = 500):
    automaton.add_body(0, 0, radius=30, mass=100 * 9999999999, name=generate_syllable())
    SPEED_COEFF = 0.004
    for _ in range(n):
        radius = random_float(0, 500)
        angle = random_float(0, 2 * math.pi)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        u = SPEED_COEFF * -y  # + random_float(-.1, .1)
        v = SPEED_COEFF * x  # + random_float(-.1, .1)
        radius = 1  # random_float(1, 10)
        mass = radius  # * 9999999999
        name = generate_syllable()
        automaton.add_body(x, y, radius=radius, mass=mass, u=u, v=v, name=name)


def spawn_line(automaton: Automaton, n: int = 100):
    SUN_RADIUS = 200
    DENSITY = 9999999999
    automaton.add_body(0, 0, radius=SUN_RADIUS, mass=SUN_RADIUS * DENSITY, name=generate_syllable())
    SPEED_COEFF = 6
    distances = numpy.linspace(SUN_RADIUS + 10, SUN_RADIUS * 10, n)
    for dist in distances:
        angle = 0  # random_float(0, 2 * math.pi)
        x = dist * math.cos(angle)
        y = dist * math.sin(angle)
        speed = SPEED_COEFF / dist**0.35
        u = -speed * math.sin(angle)
        v = speed * math.cos(angle)
        radius = random_float(1, 3)
        mass = radius  # * DENSITY
        name = generate_syllable()
        automaton.add_body(x, y, radius=radius, mass=mass, u=u, v=v, name=name)


def overlap(a: tuple[float, float], b: tuple[float, float]) -> float:
    """
    Calculate the overlap between two ranges
    :param a: (amin, amax)
    :param b: (bmin, bmax)
    :return: overlap, or 0 if no overlap
    """
    amin, amax = a
    bmin, bmax = b
    return max(0, min(amax, bmax) - max(amin, bmin))


def square_text(text: str) -> str:
    """
    Format a long string into a square block
    """
    return text
    if len(text) < 10:
        return text
    width = math.ceil(math.sqrt(len(text)))
    wrapped = []
    ii = 0
    while ii < len(text):
        wrapped.append(text[ii : ii + width])
        ii += width
    return "\n".join(wrapped)
