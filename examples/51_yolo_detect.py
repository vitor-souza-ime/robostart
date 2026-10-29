"""Example 51: Run YOLO once and print detection dictionaries.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        detections = robot.detect_objects()
        print("Detections:", detections)
