"""Example 16: Read the last commanded wheel velocities.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.set_wheel_speeds(2.0, -2.0)
    print("Commanded velocities:", robot.get_wheel_speeds())
    robot.wait(0.2)
