"""Example 30: Read the raw value of sonar 3.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("so3 raw:", robot.sonar_raw(3))
