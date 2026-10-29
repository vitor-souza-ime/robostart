"""Example 50: Load the YOLO11 nano pretrained model.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot):
        print("YOLO model loaded successfully.")
