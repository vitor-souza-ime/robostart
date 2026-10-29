"""Example 46: Read the camera image resolution.

Requires: Webots Camera. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import camera_ready
with RoboStart() as robot:
    if camera_ready(robot):
        print("Camera (width, height):", robot.camera_resolution())
