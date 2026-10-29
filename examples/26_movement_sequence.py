"""Example 26: Execute a simple forward-turn-reverse sequence.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.forward_for(0.25)
    robot.turn_left_for(0.35)
    robot.backward_for(0.25)
    print("Sequence finished at:", robot.time())
