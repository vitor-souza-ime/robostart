"""Example 41: Stop a timed forward command when a front sonar is close.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    result = robot.forward_for(0.8, safe=True, clearance_m=0.7)
    print("Clear path throughout movement:", result)
