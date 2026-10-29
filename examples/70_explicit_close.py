"""Example 70: Initialize and close the RoboStart session explicitly."""
from robostart import RoboStart

robot = RoboStart()
try:
    robot.step()
    print("Robot:", robot.robot_name)
    robot.stop()
finally:
    robot.close()
