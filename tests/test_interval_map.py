from pytest import mark, fixture
from pytest_lazyfixture import lazy_fixture

from ijim.interval_map import IntervalMap
from ijim.exceptions import (
    IntervalMapNoDuplicates,
    IntervalMapMustBeSorted,
    IntervalMapUnequalLength,
)


@fixture
def empty_im() -> IntervalMap:
    return IntervalMap[int, int](0)


@fixture
def one_ten_im() -> IntervalMap:
    return IntervalMap[int, int](0, [1, 10], [1, 10])


@mark.parametrize("default, points, vals, expected" , [
    (0, [], [], lazy_fixture('empty_im')),
    (0, [0], [0], lazy_fixture('empty_im')),
    (0, [1, 10], [1, 10], lazy_fixture('one_ten_im')),
])
def test_valid_creation(
    default: int,
    points: list[int],
    vals: list[int],
    expected: IntervalMap,
):
    assert IntervalMap(default, points, vals) == expected


@mark.parametrize("default, points, vals, exception" , [
    (0, [0, 0], [0, 0], IntervalMapNoDuplicates),
    (0, [2, 1], [1, 2], IntervalMapMustBeSorted),
    (0, [1, 2, 3], [1, 2], IntervalMapUnequalLength),
])
def test_invalid_creation(
    default: int,
    points: list[int],
    vals: list[int],
    exception: Exception,
):
    try:
        IntervalMap(default, points, vals)
    except Exception as e:
        assert e == exception


@mark.parametrize("im, key, expected" , [
    (lazy_fixture('empty_im'), 0, 0),
    (lazy_fixture('empty_im'), -1, 0),
    (lazy_fixture('empty_im'), 1, 0),
    (lazy_fixture('one_ten_im'), 0, 0),
    (lazy_fixture('one_ten_im'), 9, 1),
    (lazy_fixture('one_ten_im'), 10, 10),
])
def test_empty_getitem(im: IntervalMap, key: int, expected: int):
    val = im[key]
    assert val == expected, f"expected {expected}, got {val}"
