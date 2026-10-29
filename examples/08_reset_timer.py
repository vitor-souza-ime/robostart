"""Example 08: Reset a timer after an event.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.start_timer("lap")
    robot.wait(0.3)
    print("Before reset:", robot.timer_elapsed("lap"))
    robot.reset_timer("lap")
    print("After reset:", robot.timer_elapsed("lap"))
