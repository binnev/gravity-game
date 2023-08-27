import re
import random


STARTS = (
    "Zo",
    "Xa",
    "Ve",
    "Vil",
    "Val",
    "Quie",
    "Qua",
    "Ah",
    "Riu",
    "Ne",
    "Iya",
)


ENDS = (
    "kk",
    "rt",
    "lip",
    "rp",
    "iun",
    "ddian",
    "orant",
    "zian",
    "xian",
    "l",
    "lt",
    "n",
    "nt",
    "due",
    "sh",
)


def generate_syllable() -> str:
    """
    Generate an alien-sounding name for a planetary body
    """
    return random.choice(STARTS) + random.choice(ENDS)


def choose_new_name(left: str, right: str, massleft: float, massright: float) -> str:
    # if one body is much more massive, just continue using that name.
    # The smaller body is just absorbed into the larger one.
    if max(massleft, massright) / min(massleft, massright) > 7:
        return left if massleft > massright else right

    # non-hyphenated names
    if "-" not in left + right:
        if len(left + right) < 10:
            newname = left + right if massleft >= massright else right + left
            return newname.title()
        else:
            return f"{left}-{right}" if massleft >= massright else f"{right}-{left}"

    # merging hyphenated names
    rx = re.compile(r"(?P<first>\w+)(-(?P<second>\w+))?(-(?P<number>\d+))?")

    match = rx.search(left)
    left1 = match.group("first") or ""
    left2 = match.group("second") or ""
    leftnum = int(match.group("number") or 0)

    match = rx.search(right)
    right1 = match.group("first") or ""
    right2 = match.group("second") or ""
    rightnum = int(match.group("number") or 0)

    x = len(left2) + len(right2) + leftnum + rightnum
    if massleft >= massright:
        return f"{left1}-{right1}-{x}"
    else:
        return f"{right1}-{left1}-{x}"
