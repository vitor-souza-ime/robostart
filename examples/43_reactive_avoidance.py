"""Example 43: Short reactive obstacle avoidance with a bounded loop.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    for _ in range(35):
        if robot.obstacle_ahead(0.65):
            robot.turn_left(speed=1.4)
        else:
            robot.forward(speed=1.5)
        if not robot.step():
            break
