"""Example 62: Use YOLO and proximity sensors in the same decision.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print("Front clearance:", robot.front_distance())
        print("Visible person:", robot.object_detected("person"))
        if robot.obstacle_ahead(0.6):
            robot.stop()
            print("Too close: motors stopped")
