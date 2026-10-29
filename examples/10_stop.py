"""Example 10: Initialize and stop all four wheels.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.stop()
    print("Wheel speeds:", robot.get_wheel_speeds())
