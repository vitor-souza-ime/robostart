"""Example 01: Connect and print the robot name and basic time step.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Connected:", robot.robot_name)
    print("Basic time step (ms):", robot.timestep_ms)
    print("Initial simulated time:", robot.time())
