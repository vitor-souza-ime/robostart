"""Example 61: Record detections and confidence to CSV.

Requires: Camera + YOLO. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

import csv
from robostart import RoboStart
from _helpers import OUTPUT, vision_ready
with RoboStart() as robot:
    if vision_ready(robot):
        path = OUTPUT / "detections.csv"
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["simulation_time_s", "label", "confidence"])
            for _ in range(3):
                if not robot.step():
                    break
                for detection in robot.detect_objects():
                    writer.writerow([robot.time(), detection["label"], detection["confidence"]])
        print("Saved:", path)
