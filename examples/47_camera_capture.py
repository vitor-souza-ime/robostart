"""Example 47: Capture one BGR image as a NumPy array.

Requires: Camera + NumPy. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import camera_ready
with RoboStart() as robot:
    if camera_ready(robot) and robot.step():
        frame = robot.capture_frame()
        print("Image shape (H, W, BGR):", None if frame is None else frame.shape)
