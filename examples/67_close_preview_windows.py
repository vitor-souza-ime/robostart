"""Example 67: Explicitly close OpenCV preview windows.

Requires: Camera + NumPy + OpenCV. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import camera_ready
with RoboStart() as robot:
    if camera_ready(robot) and robot.step():
        robot.show_camera()
        robot.close_windows()
        print("Preview windows closed.")
