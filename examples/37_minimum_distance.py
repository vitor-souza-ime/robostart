"""Example 37: Compare a selected group of sonars.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    nearest = robot.minimum_distance([1, 2, 3, 4, 5, 6])
    print("Nearest in selected sector:", round(nearest, 2))
