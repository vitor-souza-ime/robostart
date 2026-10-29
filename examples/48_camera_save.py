"""Example 48: Save a captured frame to outputs/camera.png.

Requires: Camera + NumPy + OpenCV. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import OUTPUT, camera_ready
with RoboStart() as robot:
    if camera_ready(robot) and robot.step():
        robot.capture_frame()
        print("Saved:", robot.save_image(OUTPUT / "camera.png"))
