from robingame.utils import random_float

from gravity.automaton import Automaton


def create_solar_system(automaton: Automaton):
    """
    Add the bodies in our solar system
    """
    _ = ["MERCURY", "VENUS", "EARTH", "MARS", "JUPITER", "SATURN", "URANUS", "NEPTUNE", "PLUTO"]
    masses_e24 = [0.330, 4.87, 5.97, 0.642, 1898, 568, 86.8, 102, 0.013, 0]
    diameters_e3 = [4879, 12.104, 12.756, 6792, 142.984, 120.536, 51.118, 49.528, 2376]
    sun_dist_e6 = [57.9, 108.2, 149.6, 228.0, 778.5, 1432.0, 2867.0, 4515.0, 5906.4]
    velocities_e3 = [47.4, 35.0, 29.8, 24.1, 13.1, 9.7, 6.8, 5.4, 4.7]
    automaton.add_body(x=0, y=0, mass=1989100000e21, radius=695508e3)  # sun
    for mass, diameter, dist, vel in zip(masses_e24, diameters_e3, sun_dist_e6, velocities_e3):
        mass *= 1e24
        diameter *= 1e3
        dist *= 1e6
        vel *= 1e3
        automaton.add_body(x=0, y=dist, mass=mass, radius=diameter / 2, u=vel)
    # automaton.add_body(x=0, y=57.9e9, mass=0.33010e24, radius=4879e3 / 2, u=47.36e3)  # mercury
    # automaton.add_body(x=0, y=57.9e9, mass=0.33010e24, radius=4879e3 / 2, u=47.36e3)  # mercury


def spawn_random(automaton: Automaton):
    for _ in range(500):
        x = random_float(-500, 500)
        y = random_float(-500, 500)
        u = random_float(-3, 3)
        v = random_float(-3, 3)
        radius = random_float(1, 10)
        mass = radius * 9999999999
        automaton.add_body(x, y, radius=radius, mass=mass, u=u, v=v)


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
