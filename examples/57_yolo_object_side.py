"""Example 57: Determine whether an object is left, centre, or right.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        for item in robot.last_detections:
            print(item["label"], "is on the", robot.object_side(item))
