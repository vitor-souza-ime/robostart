"""Offline perception contracts using a fake YOLO model and a fake camera."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from robostart import RoboStart
from tests.fake_webots import FakeRobot


class Scalar:
    def __init__(self, value): self.value = value
    def item(self): return self.value


class Coords:
    def __init__(self, vals): self.vals = vals
    def tolist(self): return self.vals


class Box:
    def __init__(self, cls, confidence, points):
        self.cls = Scalar(cls)
        self.conf = Scalar(confidence)
        self.xyxy = [Coords(points)]


class Result:
    def __init__(self):
        self.names = {0: 'person', 1: 'chair'}
        self.boxes = [Box(0, .95, [0, 0, 2, 2]), Box(1, .7, [2, 0, 4, 2])]
    def plot(self):
        return 'fake annotated frame'


class FakeYOLO:
    def __init__(self): self.kwargs = None
    def predict(self, **kwargs):
        self.kwargs = kwargs
        return [Result()]


class VisionTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeRobot(camera=True)
        self.robot = RoboStart(backend=self.backend)
        self.robot._yolo = FakeYOLO()
        self.robot._yolo_device = None
    def tearDown(self):
        self.robot.close()

    def test_01_resolution(self):
        self.assertEqual(self.robot.camera_resolution(), (4, 2))
    def test_02_frame(self):
        try: import numpy as np
        except ImportError: self.skipTest('NumPy not available in test runtime')
        frame = self.robot.capture_frame()
        self.assertEqual(frame.shape, (2, 4, 3))
        self.assertEqual(frame[0, 0].tolist(), [0, 20, 100])
    def test_03_no_frame(self):
        self.backend.by_name['camera'].raw = None
        self.assertIsNone(self.robot.capture_frame())
    def test_04_detect_objects(self):
        data = self.robot.detect_objects(frame='dummy')
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['box'], (0, 0, 2, 2))
        self.assertGreaterEqual(self.robot.last_inference_ms, 0)
    def test_05_detection_filters(self):
        self.robot.detect_objects(frame='dummy')
        self.assertEqual(self.robot.count_objects(), 2)
        self.assertEqual(self.robot.count_objects('person'), 1)
        self.assertTrue(self.robot.object_detected('person', min_confidence=.9))
        self.assertFalse(self.robot.object_detected('chair', min_confidence=.8))
        self.assertEqual(self.robot.best_detection()['label'], 'person')
        self.assertEqual(self.robot.filter_detections('person')[0]['confidence'], .95)
    def test_06_center_and_side(self):
        self.robot.detect_objects(frame='dummy')
        person, chair = self.robot.last_detections
        self.assertEqual(self.robot.object_center(person), (1.0, 1.0))
        self.assertEqual(self.robot.object_side(person), 'left')
        self.assertEqual(self.robot.object_side(chair), 'right')
    def test_07_empty(self):
        self.assertEqual(self.robot.best_detection(), None)
        self.assertEqual(self.robot.count_objects(), 0)
    def test_08_invalid_confidence(self):
        with self.assertRaises(ValueError):
            self.robot.detect_objects(confidence=2, frame='dummy')
        with self.assertRaises(ValueError):
            self.robot.filter_detections(min_confidence=-1)
    def test_09_missing_model(self):
        self.robot._yolo = None
        with self.assertRaises(RuntimeError):
            self.robot.detect_objects(frame='dummy')
    def test_10_load_model_mock(self):
        from unittest.mock import MagicMock
        fake_ultra = MagicMock()
        with patch.dict('sys.modules', {'ultralytics': fake_ultra}):
            self.robot.load_yolo('fake.pt', device='cpu')
        fake_ultra.YOLO.assert_called_once_with('fake.pt')
        self.assertEqual(self.robot._yolo_device, 'cpu')
    def test_11_image_save_mock(self):
        from unittest.mock import MagicMock
        fake_cv = MagicMock()
        fake_cv.imwrite.return_value = True
        self.robot._annotated_frame = 'fake image'
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict('sys.modules', {'cv2': fake_cv}):
                result = self.robot.save_image(Path(folder) / 'image.png', annotated=True)
            self.assertTrue(result.endswith('image.png'))
            fake_cv.imwrite.assert_called_once()
    def test_12_image_preview_mock(self):
        from unittest.mock import MagicMock
        fake_cv = MagicMock()
        self.robot._annotated_frame = 'fake image'
        with patch.dict('sys.modules', {'cv2': fake_cv}):
            self.assertTrue(self.robot.show_camera(annotated=True))
            fake_cv.imshow.assert_called_once()
            self.robot.close_windows()
            fake_cv.destroyAllWindows.assert_called_once()
    def test_13_missing_inference_frame(self):
        self.backend.by_name['camera'].raw = None
        self.assertEqual(self.robot.detect_objects(), [])
        self.assertIsNone(self.robot._annotated_frame)
    def test_14_best_filtered(self):
        self.robot.detect_objects(frame='dummy')
        self.assertEqual(self.robot.best_detection('chair')['label'], 'chair')
        self.assertIsNone(self.robot.best_detection('bottle'))


if __name__ == '__main__':
    unittest.main()
