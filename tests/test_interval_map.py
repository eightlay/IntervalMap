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

@fixture
def alternation_im() -> IntervalMap:
    return IntervalMap[int, int](0, [1, 3, 5], [1, 0, 1])


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


@mark.parametrize("im, key, val, expected" , [
    (lazy_fixture('empty_im'), 0, 1, IntervalMap(0, [0], [1])),
    (lazy_fixture('one_ten_im'), 5, 7, IntervalMap(0, [1, 5, 10], [1, 7, 10])),
    (lazy_fixture('one_ten_im'), -1, 7, IntervalMap(0, [-1, 1, 10], [7, 1, 10])),
    (lazy_fixture('one_ten_im'), 12, 7, IntervalMap(0, [1, 10, 12], [1, 10, 7])),
    (lazy_fixture('one_ten_im'), 5, 7, IntervalMap(0, [1, 5, 10], [1, 7, 10])),
    (lazy_fixture('one_ten_im'), 0, 1, IntervalMap(0, [0, 10], [1, 10])),
    (lazy_fixture('one_ten_im'), 2, 1, IntervalMap(0, [1, 10], [1, 10])),
    (lazy_fixture('one_ten_im'), 12, 1, IntervalMap(0, [1, 10, 12], [1, 10, 1])),
    (lazy_fixture('one_ten_im'), 12, 10, IntervalMap(0, [1, 10], [1, 10])),
    (lazy_fixture('alternation_im'), -1, 3, IntervalMap(0, [-1, 1, 3, 5], [3, 1, 0, 1])),
    (lazy_fixture('alternation_im'), 2, 3, IntervalMap(0, [1, 2, 3, 5], [1, 3, 0, 1])),
    (lazy_fixture('alternation_im'), 7, 3, IntervalMap(0, [1, 3, 5, 7], [1, 0, 1, 3])),
    (lazy_fixture('alternation_im'), -1, 0, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), -1, 1, IntervalMap(0, [-1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 1, 0, IntervalMap(0, [5], [1])),
    (lazy_fixture('alternation_im'), 7, 1, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 2, 1, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 2, 0, IntervalMap(0, [1, 2, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 3, 1, IntervalMap(0, [1], [1])),
])
def test_set(im: IntervalMap, key: int, val: int, expected: IntervalMap):
    im.set(key, val)
    assert im == expected


@mark.parametrize("im, key, expected" , [
    (lazy_fixture('empty_im'), 0, IntervalMap(0, [], [])),
    (lazy_fixture('one_ten_im'), 0, IntervalMap(0, [1, 10], [1, 10])),
    (lazy_fixture('one_ten_im'), 11, IntervalMap(0, [1, 10], [1, 10])),
    (lazy_fixture('one_ten_im'), 5, IntervalMap(0, [1, 10], [1, 10])),
    (lazy_fixture('one_ten_im'), 1, IntervalMap(0, [10], [10])),
    (lazy_fixture('one_ten_im'), 10, IntervalMap(0, [1], [1])),
    (lazy_fixture('alternation_im'), -1, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 1, IntervalMap(0, [5], [1])),
    (lazy_fixture('alternation_im'), 2, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
    (lazy_fixture('alternation_im'), 3, IntervalMap(0, [1], [1])),
    (lazy_fixture('alternation_im'), 5, IntervalMap(0, [1, 3], [1, 0])),
    (lazy_fixture('alternation_im'), 6, IntervalMap(0, [1, 3, 5], [1, 0, 1])),
])
def test_unset(im: IntervalMap, key: int, expected: IntervalMap):
    im.unset(key)
    assert im == expected
