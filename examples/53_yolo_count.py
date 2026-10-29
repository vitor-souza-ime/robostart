"""Example 53: Count detected people and all objects.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print("Total objects:", robot.count_objects())
        print("People:", robot.count_objects("person"))
