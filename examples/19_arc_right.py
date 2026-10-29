"""Example 19: Steer along a shallow right arc.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.arc_right(speed=2.0, ratio=0.6)
    print("Velocities:", robot.get_wheel_speeds())
    robot.wait(0.4)
