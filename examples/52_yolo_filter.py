"""Example 52: Filter detected people from all YOLO detections.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects(confidence=0.3, image_size=320)
        print("People:", robot.filter_detections("person", min_confidence=0.4))
