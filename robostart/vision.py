"""Optional NumPy/OpenCV/Ultralytics perception helpers."""
from __future__ import annotations

from pathlib import Path
from time import perf_counter

from .errors import VisionDependencyError
from .motion import _number


def _numpy():
    try:
        import numpy as np
    except ImportError as exc:
        raise VisionDependencyError("Install optional vision packages: py -3.12 -m pip install -r requirements-vision.txt") from exc
    return np


def _opencv():
    try:
        import cv2
    except ImportError as exc:
        raise VisionDependencyError("OpenCV missing: py -3.12 -m pip install opencv-python") from exc
    return cv2


class VisionMixin:
    @property
    def camera_available(self) -> bool:
        return self._camera is not None

    def camera_resolution(self) -> tuple[int, int]:
        camera = self._require_camera()
        return int(camera.getWidth()), int(camera.getHeight())

    def capture_frame(self):
        """Capture BGR NumPy image or None before first enabled camera step."""
        camera = self._require_camera()
        raw = camera.getImage()
        if raw is None:
            return None
        np = _numpy()
        width, height = self.camera_resolution()
        # Webots camera bytes are BGRA; OpenCV/YOLO accept BGR (channel 0..2).
        frame = np.frombuffer(raw, dtype=np.uint8).reshape(height, width, 4)[:, :, :3].copy()
        self._last_frame = frame
        return frame

    def save_image(self, path, *, annotated: bool = False) -> str:
        """Save latest captured/detected frame to PNG/JPEG using OpenCV."""
        cv2 = _opencv()
        frame = self._annotated_frame if annotated else self._last_frame
        if frame is None and not annotated:
            frame = self.capture_frame()
        if frame is None:
            raise ValueError("No image available yet. Call step() then capture_frame() or detect_objects().")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if not cv2.imwrite(str(path), frame):
            raise OSError(f"Could not save image to '{path}'.")
        return str(path)

    def show_camera(self, *, annotated: bool = False, window: str = "RoboStart Camera") -> bool:
        """Show a preview window. Use close_windows() when finished."""
        cv2 = _opencv()
        frame = self._annotated_frame if annotated else self.capture_frame()
        if frame is None:
            return False
        cv2.imshow(window, frame)
        cv2.waitKey(1)
        return True

    def close_windows(self) -> None:
        # If OpenCV was never loaded, do not import it just for cleanup.
        import sys
        if "cv2" in sys.modules:
            sys.modules["cv2"].destroyAllWindows()

    def load_yolo(self, weights: str = "yolo11n.pt", *, device=None) -> None:
        """Load Ultralytics YOLO; default weights may download on first use."""
        self._require_camera()
        try:
            from ultralytics import YOLO
        except ImportError as exc:
            raise VisionDependencyError("Ultralytics missing: py -3.12 -m pip install ultralytics") from exc
        self._yolo = YOLO(weights)
        self._yolo_device = device

    def detect_objects(self, *, confidence: float = 0.35, image_size: int = 320, frame=None) -> list[dict]:
        """Run YOLO and return [{label, confidence, box}, ...].

        Coordinates of `box` are (x1, y1, x2, y2) in image pixels.
        Latency reflects wall-clock YOLO processing, not simulation time.
        """
        confidence = _number(confidence, "confidence")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be in [0, 1].")
        if isinstance(image_size, bool) or not isinstance(image_size, int) or image_size <= 0:
            raise ValueError("image_size must be a positive integer.")
        if self._yolo is None:
            raise RuntimeError("YOLO model not loaded. Call load_yolo() first.")
        if frame is None:
            frame = self.capture_frame()
        if frame is None:
            self.last_detections = []
            self._annotated_frame = None
            return []
        self._last_frame = frame
        options = {"source": frame, "conf": confidence, "imgsz": image_size, "verbose": False}
        if self._yolo_device is not None:
            options["device"] = self._yolo_device
        start = perf_counter()
        result = self._yolo.predict(**options)[0]
        self.last_inference_ms = (perf_counter() - start) * 1000
        output = []
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls.item())
                output.append({
                    "label": str(result.names[class_id]),
                    "confidence": float(box.conf.item()),
                    "box": tuple(int(v) for v in box.xyxy[0].tolist()),
                })
        self.last_detections = output
        self._annotated_frame = result.plot()
        return output

    def filter_detections(self, label: str | None = None, *, min_confidence: float = 0.0, detections=None) -> list[dict]:
        threshold = _number(min_confidence, "min_confidence")
        if not 0 <= threshold <= 1:
            raise ValueError("min_confidence must be in [0, 1].")
        items = self.last_detections if detections is None else detections
        return [d for d in items if (label is None or d["label"].lower() == label.lower())
                and d["confidence"] >= threshold]

    def object_detected(self, label: str, *, min_confidence: float = 0.0) -> bool:
        return bool(self.filter_detections(label, min_confidence=min_confidence))

    def count_objects(self, label: str | None = None) -> int:
        return len(self.filter_detections(label))

    def best_detection(self, label: str | None = None):
        items = self.filter_detections(label)
        return max(items, key=lambda item: item["confidence"]) if items else None

    @staticmethod
    def object_center(detection: dict) -> tuple[float, float]:
        x1, y1, x2, y2 = detection["box"]
        return (x1 + x2) / 2, (y1 + y2) / 2

    def object_side(self, detection: dict) -> str:
        """Location in the image: 'left', 'center', or 'right'."""
        width, _ = self.camera_resolution()
        x, _ = self.object_center(detection)
        if x < width / 3:
            return "left"
        if x > width * 2 / 3:
            return "right"
        return "center"
