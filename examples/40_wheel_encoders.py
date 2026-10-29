"""Example 40: Read wheel rotation position sensors, when present.

Requires: Webots. Run via F5 in VS Code with Webots Pioneer3at <extern>.
"""

from robostart import RoboStart
from robostart import DeviceNotFoundError
with RoboStart() as robot:
    robot.step()
    try:
        print("Encoders (rad):", robot.read_wheel_encoders())
    except DeviceNotFoundError as error:
        print("SKIPPED:", error)
