"""Shared *example-only* setup for optional vision and CSV outputs."""
from pathlib import Path
from robostart import VisionDependencyError

OUTPUT = Path(__file__).resolve().parents[1] / "outputs"
OUTPUT.mkdir(exist_ok=True)

def camera_ready(robot):
    if not robot.camera_available:
        print("SKIPPED: no camera. See docs/CAMERA_SETUP.md")
        return False
    return True

def vision_ready(robot, weights="yolo11n.pt"):
    if not camera_ready(robot):
        return False
    try:
        robot.load_yolo(weights)
        return True
    except (VisionDependencyError, OSError, ConnectionError) as exc:
        print(f"SKIPPED: YOLO unavailable: {exc}")
        return False
