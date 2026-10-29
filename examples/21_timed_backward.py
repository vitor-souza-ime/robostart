"""Example 21: Backward for a fixed duration.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Completed:", robot.backward_for(0.4, speed=1.5))
