"""Differential/skid-steer wheel controls for the Pioneer 3-AT."""

from __future__ import annotations

import math


def _number(value, name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number.") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be a finite number.")
    return result


class MotionMixin:
    def set_wheel_speeds(self, left: float, right: float) -> tuple[float, float]:
        """Set both left and both right wheel velocities in rad/s (clamped)."""
        left, right = _number(left, "left"), _number(right, "right")
        limit = self.MAX_WHEEL_SPEED
        left = max(-limit, min(limit, left))
        right = max(-limit, min(limit, right))
        for name in ("front_left", "back_left"):
            self._wheels[name].setVelocity(left)
        for name in ("front_right", "back_right"):
            self._wheels[name].setVelocity(right)
        self._wheel_speeds = (left, right)
        return self._wheel_speeds

    def get_wheel_speeds(self) -> tuple[float, float]:
        """Last commanded (left, right) wheel speeds in rad/s."""
        return self._wheel_speeds

    def forward(self, speed: float = 2.0) -> None:
        """Drive forward until another command or stop()."""
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(speed, speed)

    def backward(self, speed: float = 2.0) -> None:
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(-speed, -speed)

    def turn_left(self, speed: float = 1.5) -> None:
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(-speed, speed)

    def turn_right(self, speed: float = 1.5) -> None:
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(speed, -speed)

    def arc_left(self, speed: float = 2.0, ratio: float = 0.5) -> None:
        """Curve left: left side runs at `ratio` times right side (0..1)."""
        ratio = _number(ratio, "ratio")
        if not 0 <= ratio <= 1:
            raise ValueError("ratio must be in the range [0, 1].")
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(speed * ratio, speed)

    def arc_right(self, speed: float = 2.0, ratio: float = 0.5) -> None:
        ratio = _number(ratio, "ratio")
        if not 0 <= ratio <= 1:
            raise ValueError("ratio must be in the range [0, 1].")
        speed = abs(_number(speed, "speed"))
        self.set_wheel_speeds(speed, speed * ratio)

    def stop(self) -> None:
        self.set_wheel_speeds(0.0, 0.0)

    def move_for(
        self,
        seconds: float,
        left: float,
        right: float,
        *,
        avoid_obstacles: bool = False,
        clearance_m: float = 0.5,
    ) -> bool:
        """Move for simulation seconds and stop; False on obstacle/termination.

        Obstacle checking is designed for forward moves. The sonar scan is
        approximate, not a certified collision-avoidance mechanism.
        """
        seconds = _number(seconds, "seconds")
        if seconds < 0:
            raise ValueError("seconds must be non-negative.")
        if seconds == 0:
            self.stop()
            return True
        if avoid_obstacles:
            clearance_m = _number(clearance_m, "clearance_m")
            if clearance_m <= 0:
                raise ValueError("clearance_m must be positive.")
            if self.obstacle_ahead(clearance_m):
                self.stop()
                return False
        deadline = self.time() + seconds
        self.set_wheel_speeds(left, right)
        try:
            while self.time() + 1e-9 < deadline:
                if not self.step():
                    return False
                if avoid_obstacles and self.obstacle_ahead(clearance_m):
                    return False
            return True
        finally:
            self.stop()

    def forward_for(self, seconds: float, speed: float = 2.0, *, safe: bool = True,
                    clearance_m: float = 0.5) -> bool:
        speed = abs(_number(speed, "speed"))
        return self.move_for(seconds, speed, speed,
                             avoid_obstacles=safe, clearance_m=clearance_m)

    def backward_for(self, seconds: float, speed: float = 2.0) -> bool:
        speed = abs(_number(speed, "speed"))
        return self.move_for(seconds, -speed, -speed)

    def turn_left_for(self, seconds: float, speed: float = 1.5) -> bool:
        speed = abs(_number(speed, "speed"))
        return self.move_for(seconds, -speed, speed)

    def turn_right_for(self, seconds: float, speed: float = 1.5) -> bool:
        speed = abs(_number(speed, "speed"))
        return self.move_for(seconds, speed, -speed)
