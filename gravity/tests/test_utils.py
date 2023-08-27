from redbreast.testing import parametrize, testparams

from gravity.utils import overlap


@parametrize(
    param := testparams("a", "b", "expected"),
    [
        param(
            description="same range",
            a=(0, 10),
            b=(0, 10),
            expected=10,
        ),
        param(
            description="no overlap should return 0",
            a=(0, 10),
            b=(11, 20),
            expected=0,
        ),
        param(
            description="no overlap should return 0 (b < a)",
            a=(11, 20),
            b=(0, 10),
            expected=0,
        ),
        param(
            description="some overlap (a < b)",
            a=(0, 10),
            b=(5, 15),
            expected=5,
        ),
        param(
            description="some overlap (b < a)",
            a=(5, 15),
            b=(0, 10),
            expected=5,
        ),
        param(
            description="float overlap (a < b)",
            a=(0, 10.2),
            b=(5.6, 15),
            expected=4.6,
        ),
        param(
            description="ends touching should give 0",
            a=(0, 10.2),
            b=(10.2, 15),
            expected=0,
        ),
    ],
)
def test_overlap(param):
    assert overlap(param.a, param.b) == param.expected
