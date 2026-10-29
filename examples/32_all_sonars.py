"""Example 32: Read all 16 Pioneer sonar sensors.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    for index, distance in robot.read_all_sonars().items():
        print(f"so{index:02d}: {distance:.2f} m")
