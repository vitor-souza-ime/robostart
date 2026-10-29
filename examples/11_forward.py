"""Example 11: Move forward and stop.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.forward(speed=1.5)
    robot.wait(0.35)
    robot.stop()
