"""Example 31: Read an approximate sonar distance in metres.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("so3 distance (m):", round(robot.sonar_distance(3), 2))
