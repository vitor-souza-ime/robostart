"""Example 24: Timed differential movement with explicit wheel speeds.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Completed:", robot.move_for(0.4, left=1.0, right=2.0))
