"""Example 63: Drive slowly, then stop when a person is detected.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot):
        for _ in range(4):
            if not robot.step():
                break
            robot.detect_objects()
            if robot.object_detected("person") or robot.obstacle_ahead(0.7):
                robot.stop()
                print("Stopping because of vision or sonar")
                break
            robot.forward(speed=0.6)
