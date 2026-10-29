"""Example 12: Move backward and stop.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.backward(speed=1.3)
    robot.wait(0.35)
    robot.stop()
