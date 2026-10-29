"""Example 68: Self-check main commands without requiring vision packages.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
with RoboStart() as robot:
    robot.step()
    checks = {
        "robot_connected": bool(robot.robot_name),
        "four_motors": robot.info()["wheels"] == 4,
        "sixteen_sonars": len(robot.read_all_sonars()) == 16,
        "time_available": robot.time() >= 0,
        "safe_stop": robot.get_wheel_speeds() == (0, 0),
        "camera_optional": isinstance(robot.camera_available, bool),
    }
    for name, passed in checks.items():
        print(("PASS" if passed else "FAIL"), name)
