"""Example 20: Forward for a fixed duration, checking front sonars.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    completed = robot.forward_for(0.5, speed=1.5, safe=True)
    print("Movement completed:", completed)
