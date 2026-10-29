"""Example 13: Turn left using skid steering.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.turn_left(speed=1.4)
    robot.wait(0.35)
    robot.stop()
