"""Example 64: Rotate briefly in search of a person.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot):
        for _ in range(6):
            if not robot.step():
                break
            robot.detect_objects()
            if robot.object_detected("person"):
                print("Person found, stopping search")
                break
            robot.turn_left_for(0.1, speed=1.0)
