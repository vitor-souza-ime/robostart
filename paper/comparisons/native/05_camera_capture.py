from pathlib import Path
from controller import Robot
import numpy as np
import cv2
robot = Robot()
dt = int(robot.getBasicTimeStep())
camera = robot.getDevice("camera")
camera.enable(dt)
if robot.step(dt) != -1:
    raw = camera.getImage()
    if raw is not None:
        width = camera.getWidth()
        height = camera.getHeight()
        frame = np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 4)[:, :, :3].copy()
        path = Path("outputs/camera.png")
        path.parent.mkdir(parents=True, exist_ok=True)
        print("Saved:", path)
        cv2.imwrite(str(path), frame)
