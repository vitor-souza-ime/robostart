"""RoboStart Webots adapter for the default Pioneer 3-AT PROTO.

The Webots `controller` module is imported only during instance construction,
so the library can be imported by editors and unit tests outside Webots.
"""

from __future__ import annotations

from .errors import CameraNotAvailableError, DeviceNotFoundError, RoboStartError
from .motion import MotionMixin
from .sensors import SensorMixin
from .timing import TimingMixin
from .vision import VisionMixin


class RoboStart(MotionMixin, TimingMixin, SensorMixin, VisionMixin):
    """Beginner-friendly Webots Pioneer 3-AT controller.

    Wheel speeds use radians per second; durations use *simulation seconds*.
    Optional camera must be named ``camera`` (configurable). A real Webots
    controller process is required unless a test backend is injected.
    """

    MAX_WHEEL_SPEED = 6.4  # Pioneer3at.proto motor maxVelocity (rad/s)
    SONAR_MAX_RANGE_M = 5.0
    SONAR_RAW_MAX = 1024.0
    FRONT_SONARS = (2, 3, 4, 5)
    LEFT_SONARS = (0, 1, 2, 3)
    RIGHT_SONARS = (4, 5, 6, 7)
    REAR_SONARS = (10, 11, 12, 13)
    WHEEL_DEVICES = {
        "front_left": "front left wheel",
        "back_left": "back left wheel",
        "front_right": "front right wheel",
        "back_right": "back right wheel",
    }

    def __init__(self, *, camera_name: str = "camera", backend=None):
        if backend is None:
            try:
                from controller import Robot  # Webots' bundled API; not a pip package
            except ImportError as exc:
                raise RoboStartError(
                    "Webots Python API not found. Run through webots-controller.exe "
                    "with the robot controller set to <extern>."
                ) from exc
            backend = Robot()
        self._robot = backend
        self.timestep_ms = int(backend.getBasicTimeStep())
        if self.timestep_ms <= 0:
            raise RoboStartError("The Webots basic time step must be positive.")
        self.robot_name = str(backend.getName())
        self._active = True
        self._timers = {}
        self._wheel_speeds = (0.0, 0.0)

        self._devices = {}
        for index in range(int(backend.getNumberOfDevices())):
            device = backend.getDeviceByIndex(index)
            self._devices[device.getName()] = device

        self._wheels = {}
        for label, name in self.WHEEL_DEVICES.items():
            motor = self._devices.get(name)
            if motor is None:
                raise DeviceNotFoundError(
                    f"Missing '{name}'. Select the standard Webots Pioneer3at PROTO."
                )
            motor.setPosition(float("inf"))
            motor.setVelocity(0.0)
            self._wheels[label] = motor

        self._sonars = {}
        for index in range(16):
            name = f"so{index}"
            sensor = self._devices.get(name)
            if sensor is None:
                raise DeviceNotFoundError(f"Missing Pioneer sonar '{name}'.")
            sensor.enable(self.timestep_ms)
            self._sonars[index] = sensor

        self._encoders = {}
        for label, wheel_name in self.WHEEL_DEVICES.items():
            encoder = self._devices.get(wheel_name + " sensor")
            if encoder is not None:
                encoder.enable(self.timestep_ms)
                self._encoders[label] = encoder

        self._camera = self._devices.get(camera_name)
        if self._camera is not None:
            if not all(hasattr(self._camera, x) for x in ("enable", "getImage", "getWidth", "getHeight")):
                raise RoboStartError(f"Device '{camera_name}' is not a Webots Camera.")
            self._camera.enable(self.timestep_ms)
        self._camera_name = camera_name
        self._yolo = None
        self._last_frame = None
        self._annotated_frame = None
        self.last_detections = []
        self.last_inference_ms = None

    def list_devices(self) -> list[str]:
        """Return names of devices visible to the current controller."""
        return sorted(self._devices)

    def info(self) -> dict:
        """Return controller and device summary."""
        return {
            "robot": self.robot_name,
            "timestep_ms": self.timestep_ms,
            "wheels": len(self._wheels),
            "sonars": len(self._sonars),
            "encoders": len(self._encoders),
            "camera": self.camera_available,
        }

    def step(self, count: int = 1) -> bool:
        """Advance the simulation by `count` basic steps; False if terminated."""
        if isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ValueError("count must be a non-negative integer.")
        if not self._active:
            return False
        for _ in range(count):
            if self._robot.step(self.timestep_ms) == -1:
                self._active = False
                return False
        return True

    def close(self) -> None:
        """Stop all motors and close any OpenCV preview windows."""
        self.stop()
        self.close_windows()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

    def _require_camera(self):
        if self._camera is None:
            raise CameraNotAvailableError(
                f"Add a Webots Camera named '{self._camera_name}' to "
                "Pioneer3at.extensionSlot. See docs/CAMERA_SETUP.md."
            )
        return self._camera
