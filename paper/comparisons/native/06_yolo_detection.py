from controller import Robot
from ultralytics import YOLO
import numpy as np
from time import perf_counter
robot = Robot()
dt = int(robot.getBasicTimeStep())
camera = robot.getDevice("camera")
camera.enable(dt)
model = YOLO("yolo11n.pt")
if robot.step(dt) != -1:
    raw = camera.getImage()
    if raw is not None:
        frame = np.frombuffer(raw, dtype=np.uint8).reshape(camera.getHeight(), camera.getWidth(), 4)[:, :, :3].copy()
        begin = perf_counter()
        result = model.predict(source=frame, conf=0.35, imgsz=320, verbose=False)[0]
        latency_ms = (perf_counter() - begin) * 1000
        detected = []
        if result.boxes is not None:
            for box in result.boxes:
                detected.append({"label": str(result.names[int(box.cls.item())]), "confidence": float(box.conf.item()), "box": tuple(int(x) for x in box.xyxy[0].tolist())})
        print("Detections:", detected)
