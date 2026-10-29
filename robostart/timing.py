"""Time helpers: Webots simulation time, not time.sleep()."""
from __future__ import annotations
from .motion import _number


class TimingMixin:
    def time(self) -> float:
        """Get elapsed simulation time in seconds."""
        return float(self._robot.getTime())

    def wait(self, seconds: float) -> bool:
        """Advance simulated seconds with the robot stationary or moving."""
        seconds = _number(seconds, "seconds")
        if seconds < 0:
            raise ValueError("seconds must be non-negative.")
        deadline = self.time() + seconds
        while self.time() + 1e-9 < deadline:
            if not self.step():
                return False
        return True

    def start_timer(self, name: str = "default") -> None:
        self._timers[name] = self.time()

    def timer_elapsed(self, name: str = "default") -> float:
        if name not in self._timers:
            raise KeyError(f"Timer '{name}' has not been started.")
        return max(0.0, self.time() - self._timers[name])

    def timer_expired(self, seconds: float, name: str = "default") -> bool:
        seconds = _number(seconds, "seconds")
        if seconds < 0:
            raise ValueError("seconds must be non-negative.")
        return self.timer_elapsed(name) >= seconds

    def reset_timer(self, name: str = "default") -> None:
        if name not in self._timers:
            raise KeyError(f"Timer '{name}' has not been started.")
        self._timers[name] = self.time()
