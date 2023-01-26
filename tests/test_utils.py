from pytest import mark

from ijim.utils import (
    is_sorted,
    has_duplicates,
)


@mark.parametrize("array, expected", [
    ([1, 2, 3], True),
    ([2, 1, 3], False),
])
def test_is_sorted(array: list, expected: bool):
    assert is_sorted(array) == expected, expected


@mark.parametrize("array, expected", [
    ([1, 2, 3], False),
    ([1, 1, 3], True),
])
def test_has_duplicates(array: list, expected: bool):
    assert has_duplicates(array) == expected, expected
