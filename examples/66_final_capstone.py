"""Example 66: Integrate time, sonars, motion, optional camera and YOLO.

Requires: Camera + YOLO optional. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from _helpers import vision_ready
with RoboStart() as robot:
    print("Robot:", robot.robot_name, "| Devices:", len(robot.list_devices()))
    robot.start_timer("mission")
    robot.step()
    print("Initial front distance:", round(robot.front_distance(), 2), "m")
    print("Safe movement:", robot.forward_for(0.3, speed=1.0, safe=True))
    if vision_ready(robot) and robot.step():
        objects = robot.detect_objects()
        print("YOLO objects:", len(objects), "| latency ms:", robot.last_inference_ms)
        if robot.object_detected("person"):
            robot.stop()
    print("Mission simulated duration:", round(robot.timer_elapsed("mission"), 2))
