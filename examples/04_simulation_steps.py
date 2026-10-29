"""Example 04: Advance multiple basic steps.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Step 1:", robot.step())
    print("Next 5 steps:", robot.step(5))
    print("Simulated seconds:", round(robot.time(), 3))
