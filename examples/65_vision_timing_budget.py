"""Example 65: Compare YOLO wall-clock latency with timestep duration.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    if vision_ready(robot) and robot.step():
        robot.detect_objects()
        print(f"Webots step: {robot.timestep_ms} ms of simulation")
        print(f"YOLO execution: {robot.last_inference_ms:.1f} ms wall-clock")
        print("These clocks are different and should not be confused.")
