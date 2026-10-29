"""Run all incremental lessons with fake Webots, OpenCV, and YOLO.

This is an OFFLINE SMOKE TEST, NOT a claim that physical/Webots simulation
was tested. Vision examples may be skipped if NumPy is not installed.
"""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch
import ast
import importlib.util
import inspect
import runpy
import sys
import types
import unittest

from robostart import RoboStart
from tests.fake_webots import FakeRobot
from tests.test_vision import Result

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / 'examples'
SCRIPTS = sorted(EXAMPLES.glob('[0-9][0-9]_*.py'))


class ExampleSmokeTests(unittest.TestCase):
    def test_000_catalog_and_public_api_coverage(self):
        self.assertGreaterEqual(len(SCRIPTS), 50)
        all_calls = set()
        for script in SCRIPTS:
            parsed = ast.parse(script.read_text(encoding='utf-8'), str(script))
            all_calls.update(node.func.attr for node in ast.walk(parsed)
                             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute))
        public = {name for name, fn in inspect.getmembers(RoboStart, predicate=inspect.isfunction)
                  if not name.startswith('_')}
        self.assertEqual(public - all_calls, set(), 'Public functions missing from lesson catalog')


def _build_lesson_test(script):
    def test_lesson(self):
        has_numpy = importlib.util.find_spec('numpy') is not None
        fake_controller = types.ModuleType('controller')
        fake_controller.Robot = lambda: FakeRobot(camera=has_numpy)

        class FakeYOLO:
            def __init__(self, *_args, **_kwargs): pass
            def predict(self, **_kwargs): return [Result()]

        fake_ultralytics = types.ModuleType('ultralytics')
        fake_ultralytics.YOLO = FakeYOLO
        fake_cv2 = types.ModuleType('cv2')
        fake_cv2.imwrite = lambda *args: True
        fake_cv2.imshow = lambda *args: None
        fake_cv2.waitKey = lambda *args: -1
        fake_cv2.destroyAllWindows = lambda: None
        with patch.dict('sys.modules', {
            'controller': fake_controller,
            'ultralytics': fake_ultralytics,
            'cv2': fake_cv2,
        }):
            with patch.object(sys, 'path', [str(ROOT), str(EXAMPLES)] + sys.path):
                output = StringIO()
                with redirect_stdout(output):
                    runpy.run_path(str(script), run_name='__main__')
                self.assertNotIn('FAIL', output.getvalue())
    return test_lesson


for script in SCRIPTS:
    setattr(ExampleSmokeTests, 'test_' + script.stem, _build_lesson_test(script))


if __name__ == '__main__':
    unittest.main()
