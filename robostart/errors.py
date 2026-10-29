"""User-friendly exceptions for RoboStart."""


class RoboStartError(RuntimeError):
    """A RoboStart operation could not be completed."""


class DeviceNotFoundError(RoboStartError):
    """A required Webots device is not configured."""


class CameraNotAvailableError(RoboStartError):
    """The Pioneer has no compatible camera in the current world."""


class VisionDependencyError(RoboStartError):
    """An optional computer-vision dependency is not installed."""
