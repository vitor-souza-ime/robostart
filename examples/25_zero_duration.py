"""Example 25: A zero-duration movement does not move the robot.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.forward(speed=2.0)
    print("Zero-duration status:", robot.move_for(0, 2.0, 2.0))
    print("Stopped:", robot.get_wheel_speeds())
