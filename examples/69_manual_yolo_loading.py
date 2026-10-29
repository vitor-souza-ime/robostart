"""Example 69: Load YOLO directly with informative optional-dependency handling."""
from robostart import RoboStart, VisionDependencyError
from _helpers import camera_ready

with RoboStart() as robot:
    if camera_ready(robot):
        try:
            robot.load_yolo("yolo11n.pt")
            print("YOLO is ready for object detection.")
        except (VisionDependencyError, OSError, ConnectionError) as error:
            print("SKIPPED: YOLO model unavailable:", error)
