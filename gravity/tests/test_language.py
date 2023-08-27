from redbreast.testing import parametrize, testparams

from gravity.language import choose_new_name


@parametrize(
    param := testparams("name1", "name2", "mass1", "mass2", "expected"),
    [
        param(
            description="mass1 >> mass2",
            name1="Zog",
            name2="Mat",
            mass1=10,
            mass2=1,
            expected="Zog",
        ),
        param(
            description="Short names, same mass",
            name1="Zog",
            name2="Mat",
            mass1=1,
            mass2=1,
            expected="Zogmat",
        ),
        param(
            description="Short names, different mass",
            name1="Zog",
            name2="Mat",
            mass1=1,
            mass2=2,
            expected="Matzog",
        ),
        param(
            description="Longer names, same mass",
            name1="Zogwartio",
            name2="Matfrunkk",
            mass1=1,
            mass2=1,
            expected="Zogwartio-Matfrunkk",
        ),
        param(
            description="Longer names, different mass",
            name1="Zogwartio",
            name2="Matfrunkk",
            mass1=1,
            mass2=2,
            expected="Matfrunkk-Zogwartio",
        ),
        param(
            description="Hyphenated names, same mass",
            name1="Zogwartio-ffff",
            name2="Flarble-ffff",
            mass1=1,
            mass2=1,
            expected="Zogwartio-Flarble-8",
        ),
        param(
            description="Hyphenated names, different mass",
            name1="Zogwartio-fffff",
            name2="Flarble-fffff",
            mass1=1,
            mass2=2,
            expected="Flarble-Zogwartio-10",
        ),
        param(
            description="One hyphenated, one non-hyphenated, different mass",
            name1="Zogwartio-fffff",
            name2="Flarble",
            mass1=1,
            mass2=2,
            expected="Flarble-Zogwartio-5",
        ),
        param(
            description="Hyphenated and numbered names",
            name1="Flarble-Bazbaz-10",
            name2="Zogwartio-Foobar-5",
            mass1=1,
            mass2=2,
            expected="Zogwartio-Flarble-27",
        ),
        param(
            description="Hyphenated and numbered name, hyphenated name",
            name1="Flarble-Bazbaz-10",
            name2="Zogwartio-Foobar",
            mass1=1,
            mass2=2,
            expected="Zogwartio-Flarble-22",
        ),
        param(
            description="Hyphenated and numbered name, normal name",
            name1="Flarble-Bazbaz-10",
            name2="Zogwartio",
            mass1=1,
            mass2=2,
            expected="Zogwartio-Flarble-16",
        ),
    ],
)
def test_choose_new_name(param):
    assert choose_new_name(param.name1, param.name2, param.mass1, param.mass2) == param.expected
