"""Example 06: Start and read an activity timer.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.start_timer("activity")
    robot.wait(0.3)
    print("Activity time:", round(robot.timer_elapsed("activity"), 3))
