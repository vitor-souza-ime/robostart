"""Example 49: Open an OpenCV camera preview for one simulated second.

Requires: Camera + NumPy + OpenCV. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import camera_ready
with RoboStart() as robot:
    if camera_ready(robot):
        robot.start_timer("preview")
        while not robot.timer_expired(1.0, "preview") and robot.step():
            robot.show_camera()
