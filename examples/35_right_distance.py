"""Example 35: Read nearest obstacle on front-right side.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Right clearance:", round(robot.right_distance(), 2), "m")
