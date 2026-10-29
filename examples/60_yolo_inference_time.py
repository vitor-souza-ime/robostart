"""Example 60: Print measured YOLO inference latency.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print(f"YOLO execution: {robot.last_inference_ms:.1f} ms (wall clock)")
