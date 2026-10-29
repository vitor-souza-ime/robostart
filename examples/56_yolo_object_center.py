"""Example 56: Get the centre of the strongest bounding box.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        best = robot.best_detection()
        print("Centre (x, y) pixels:", robot.object_center(best) if best else "No detection")
