"""Example 09: Measure nested phases with separate timers.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.start_timer("total")
    robot.wait(0.2)
    robot.start_timer("phase2")
    robot.wait(0.3)
    print("Total:", robot.timer_elapsed("total"))
    print("Phase 2:", robot.timer_elapsed("phase2"))
