"""Example 28: Repeat an action with a for loop.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    for index in range(3):
        robot.turn_right_for(0.2)
        robot.wait(0.1)
        print("Turn", index + 1, "at", robot.time())
