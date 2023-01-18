import copy
import bisect
from typing import Iterable, Generic, TypeVar

from comparable import Comparable
from utils import (
    is_sorted,
    has_duplicates,
)
from exceptions import (
    IntervalMapUnequalLength,
    IntervalMapMustBeSorted,
    IntervalMapNoDuplicates,
)


ComparableKey = TypeVar("ComparableKey", bound=Comparable)
AnyValueType = TypeVar("AnyValueType")


class IntervalMap(Generic[ComparableKey, AnyValueType]):
    def __init__(
        self,
        default_val: AnyValueType,
        interval_left_points: Iterable[ComparableKey] = [],
        vals: Iterable[AnyValueType] = [],
    ) -> None:
        if has_duplicates(interval_left_points):
            raise IntervalMapNoDuplicates
        if not is_sorted(interval_left_points):
            raise IntervalMapMustBeSorted
        if len(interval_left_points) != len(vals):
            raise IntervalMapUnequalLength

        self._lpoints = list(copy.deepcopy(interval_left_points))
        self._vals = [copy.deepcopy(default_val)] + list(copy.deepcopy(vals))

    def __getitem__(self, key: ComparableKey) -> AnyValueType:
        return self.get(key)

    def get(self, key: ComparableKey) -> AnyValueType:
        return self._vals[bisect.bisect(self._lpoints, key)]

    def __setitem__(self, key: ComparableKey, val: AnyValueType) -> None:
        self.set(key, val)

    def set(self, key: ComparableKey, val: AnyValueType) -> None:
        ind = bisect.bisect(self._lpoints, key)

        if ind >= len(self._lpoints):
            self._lpoints.append(key)
            self._vals.append(val)

        if self._lpoints[ind] == key:
            self._vals[ind + 1] = val
        else:
            self._lpoints.insert(ind, key)
            self._vals.insert(ind + 1, val)

    def __delitem__(self, key: ComparableKey) -> bool:
        self.unset(key)

    def unset(self, key: ComparableKey) -> bool:
        ind = bisect.bisect_left(self._lpoints, key)

        if ind >= len(self._lpoints):
            return False
        elif self._lpoints[ind] == key:
            del self._lpoints[ind]
            del self._vals[ind + 1]
            return True
        return False
