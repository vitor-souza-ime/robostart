"""RoboStart: beginner-friendly educational robotics for Webots Pioneer 3-AT."""
from .robot import RoboStart
from .errors import (RoboStartError, DeviceNotFoundError,
                     CameraNotAvailableError, VisionDependencyError)

__version__ = "0.1.0"
__all__ = ["RoboStart", "RoboStartError", "DeviceNotFoundError",
           "CameraNotAvailableError", "VisionDependencyError"]
