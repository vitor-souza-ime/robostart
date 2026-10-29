"""Pioneer 3-AT sonars and wheel position sensors."""
from __future__ import annotations

from .motion import _number
from .errors import DeviceNotFoundError


class SensorMixin:
    def sonar_raw(self, index: int) -> float:
        if isinstance(index, bool) or not isinstance(index, int) or index not in self._sonars:
            raise ValueError("Sonar index must be an integer from 0 to 15.")
        return float(self._sonars[index].getValue())

    def sonar_distance(self, index: int) -> float:
        """Approximate metres from Webots Pioneer sonar lookupTable.

        The standard lookupTable is 0m=>1024 and 5m=>0. This mapping does
        not apply to real sonar or other Webots robots. Far values saturate.
        """
        raw = max(0.0, min(self.SONAR_RAW_MAX, self.sonar_raw(index)))
        return self.SONAR_MAX_RANGE_M * (1.0 - raw / self.SONAR_RAW_MAX)

    def read_all_sonars(self) -> dict[int, float]:
        return {index: self.sonar_distance(index) for index in range(16)}

    def minimum_distance(self, indices) -> float:
        """Closest approximate distance among the specified sonar indices."""
        indices = tuple(indices)
        if not indices:
            raise ValueError("At least one sonar index is required.")
        return min(self.sonar_distance(i) for i in indices)

    def front_distance(self) -> float:
        return self.minimum_distance(self.FRONT_SONARS)

    def left_distance(self) -> float:
        return self.minimum_distance(self.LEFT_SONARS)

    def right_distance(self) -> float:
        return self.minimum_distance(self.RIGHT_SONARS)

    def rear_distance(self) -> float:
        return self.minimum_distance(self.REAR_SONARS)

    def obstacle_ahead(self, threshold_m: float = 0.5) -> bool:
        return self.front_distance() < _positive(threshold_m)

    def obstacle_left(self, threshold_m: float = 0.5) -> bool:
        return self.left_distance() < _positive(threshold_m)

    def obstacle_right(self, threshold_m: float = 0.5) -> bool:
        return self.right_distance() < _positive(threshold_m)

    def read_wheel_encoders(self) -> dict[str, float]:
        """Read wheel rotation positions in radians, when available."""
        if not self._encoders:
            raise DeviceNotFoundError("Wheel position sensors are unavailable.")
        return {name: float(encoder.getValue()) for name, encoder in self._encoders.items()}


def _positive(value):
    number = _number(value, "threshold_m")
    if number <= 0:
        raise ValueError("threshold_m must be positive.")
    return number
