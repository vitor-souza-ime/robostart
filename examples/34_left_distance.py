"""Example 34: Read nearest obstacle on front-left side.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Left clearance:", round(robot.left_distance(), 2), "m")
