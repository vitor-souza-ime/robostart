"""Example 39: Compare left and right obstacle flags.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    print("Obstacle left?", robot.obstacle_left(0.6))
    print("Obstacle right?", robot.obstacle_right(0.6))
