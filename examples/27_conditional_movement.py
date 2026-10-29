"""Example 27: Use if/else with robot movement.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    if robot.front_distance() > 0.8:
        robot.forward_for(0.3)
    else:
        print("Not moving: obstacle nearby")
