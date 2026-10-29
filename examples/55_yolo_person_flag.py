"""Example 55: Test whether YOLO currently detects a person.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print("Person detected:", robot.object_detected("person", min_confidence=0.4))
