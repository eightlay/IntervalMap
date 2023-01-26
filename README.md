# InfiniteJest: Interval map package

IntervalMap maps value to some interval. It has default left value.

Example:
```
    (-inf, 1) -> 0

    [1, 4) -> 3

    [4, 7) -> 10

    [7, +inf) -> 17
```

## Installation
`pip install ijim`


## Usage
Basic usage:

```
>>> im = IntervalMap[int, int](-4, [1, 10], [2, 20])
>>> for i in [-13345, 0, 5, 9, 10, 2242]:
...     print(f"{i} -> {im[i]}")
-13345 -> -4
0 -> -4
5 -> 2
9 -> 2
10 -> 20
2242 -> 20
```

You can find examples [here](https://github.com/eightlay/IntervalMap/tree/main/examples)