"""Example 33: Read the nearest obstacle in front.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Front clearance:", round(robot.front_distance(), 2), "m")
