"""Example 42: Choose a direction based on left/right sensor readings.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    if robot.left_distance() >= robot.right_distance():
        print("Turning toward clearer left side")
        robot.turn_left_for(0.35)
    else:
        print("Turning toward clearer right side")
        robot.turn_right_for(0.35)
