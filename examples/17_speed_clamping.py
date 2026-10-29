"""Example 17: Observe automatic clamping to the Pioneer motor limit.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Maximum:", robot.MAX_WHEEL_SPEED, "rad/s")
    print("Applied:", robot.set_wheel_speeds(100.0, -100.0))
    robot.wait(0.15)
