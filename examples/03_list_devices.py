"""Example 03: List available Webots motors, sensors, and camera.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    for name in robot.list_devices():
        print(name)
