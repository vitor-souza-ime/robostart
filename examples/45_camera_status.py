"""Example 45: Check whether the Pioneer camera is installed.

Requires: Camera optional. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    print("Camera available:", robot.camera_available)
