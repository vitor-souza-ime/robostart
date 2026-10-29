"""Example 59: Save a YOLO bounding-box visualization.

Requires: Camera + YOLO + OpenCV. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import OUTPUT, vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print("Saved:", robot.save_image(OUTPUT / "yolo_annotated.png", annotated=True))
