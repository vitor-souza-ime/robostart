"""Example 07: Check whether a named timer has expired.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.start_timer("trial")
    while not robot.timer_expired(0.4, "trial"):
        if not robot.step():
            break
    print("Expired:", robot.timer_expired(0.4, "trial"))
