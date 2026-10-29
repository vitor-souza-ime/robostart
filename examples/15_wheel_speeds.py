"""Example 15: Command left/right wheel groups directly.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    left, right = robot.set_wheel_speeds(1.0, 2.0)
    print("Applied (rad/s):", left, right)
    robot.wait(0.3)
