"""Example 58: Display a YOLO-annotated image.

Requires: Camera + YOLO + OpenCV. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        robot.show_camera(annotated=True, window="RoboStart YOLO")
        robot.wait(0.5)
