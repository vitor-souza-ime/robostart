"""Example 05: Wait using simulated time (not time.sleep).

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    before = robot.time()
    robot.wait(0.5)
    print("Elapsed simulated seconds:", round(robot.time() - before, 3))
