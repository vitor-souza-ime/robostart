"""Example 38: Test whether the front corridor is clear.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Obstacle ahead?", robot.obstacle_ahead(0.6))
