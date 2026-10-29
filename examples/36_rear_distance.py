"""Example 36: Read the closest rear-facing obstacle.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Rear clearance:", round(robot.rear_distance(), 2), "m")
