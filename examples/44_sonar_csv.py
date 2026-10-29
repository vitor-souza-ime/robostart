"""Example 44: Write a short sonar time series to CSV.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

import csv
from robostart import RoboStart
from _helpers import OUTPUT
with RoboStart() as robot:
    path = OUTPUT / "sonar_log.csv"
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["simulation_time_s", "front_distance_m"])
        for _ in range(20):
            if not robot.step():
                break
            writer.writerow([robot.time(), robot.front_distance()])
    print("Saved:", path)
