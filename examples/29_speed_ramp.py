"""Example 29: Increase commanded wheel speeds gradually.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    for speed in (0.5, 1.0, 1.5, 2.0):
        robot.forward(speed)
        robot.wait(0.15)
        print("Speed:", speed)
