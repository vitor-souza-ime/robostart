"""Offline RoboStart tests. No installed Webots is needed."""
import math
import unittest

from robostart import RoboStart, DeviceNotFoundError, CameraNotAvailableError
from tests.fake_webots import FakeRobot


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.backend = FakeRobot()
        self.robot = RoboStart(backend=self.backend)
    def tearDown(self):
        self.robot.close()

    def test_01_initialization(self):
        self.assertEqual(self.robot.robot_name, 'Pioneer 3-AT')
        self.assertEqual(self.robot.timestep_ms, 32)
        self.assertEqual(self.robot.info()['sonars'], 16)
        self.assertIn('so0', self.robot.list_devices())
        self.assertFalse(self.robot.camera_available)
    def test_02_motor_configuration(self):
        for wheel in self.robot.WHEEL_DEVICES.values():
            self.assertTrue(math.isinf(self.backend.by_name[wheel].position))
            self.assertEqual(self.backend.by_name[wheel].velocity, 0)
    def test_03_step_and_time(self):
        self.assertTrue(self.robot.step(2))
        self.assertAlmostEqual(self.robot.time(), .064)
    def test_04_invalid_steps(self):
        for count in (-1, 2.5, True):
            with self.assertRaises(ValueError): self.robot.step(count)
    def test_05_wait(self):
        self.assertTrue(self.robot.wait(.35))
        self.assertGreaterEqual(self.robot.time(), .35)
    def test_06_invalid_wait(self):
        with self.assertRaises(ValueError): self.robot.wait(-1)
    def test_07_timers(self):
        self.robot.start_timer('A')
        self.robot.wait(.1)
        self.assertTrue(self.robot.timer_expired(.09, 'A'))
        self.assertGreaterEqual(self.robot.timer_elapsed('A'), .1)
        self.robot.reset_timer('A')
        self.assertEqual(self.robot.timer_elapsed('A'), 0)
    def test_08_missing_timer(self):
        with self.assertRaises(KeyError): self.robot.timer_elapsed('missing')
        with self.assertRaises(KeyError): self.robot.reset_timer('missing')
    def test_09_speed_groups(self):
        self.assertEqual(self.robot.set_wheel_speeds(1, 2), (1, 2))
        for label in ('front_left', 'back_left'):
            self.assertEqual(self.robot._wheels[label].velocity, 1)
        for label in ('front_right', 'back_right'):
            self.assertEqual(self.robot._wheels[label].velocity, 2)
        self.assertEqual(self.robot.get_wheel_speeds(), (1, 2))
    def test_10_clamp_and_invalid(self):
        self.assertEqual(self.robot.set_wheel_speeds(100, -100), (6.4, -6.4))
        with self.assertRaises(ValueError): self.robot.set_wheel_speeds(float('nan'), 1)
    def test_11_motion_directions(self):
        self.robot.forward(2)
        self.assertEqual(self.robot.get_wheel_speeds(), (2, 2))
        self.robot.backward(2)
        self.assertEqual(self.robot.get_wheel_speeds(), (-2, -2))
        self.robot.turn_left(2)
        self.assertEqual(self.robot.get_wheel_speeds(), (-2, 2))
        self.robot.turn_right(2)
        self.assertEqual(self.robot.get_wheel_speeds(), (2, -2))
        self.robot.stop()
        self.assertEqual(self.robot.get_wheel_speeds(), (0, 0))
    def test_12_arc_left_right(self):
        self.robot.arc_left(2, .5)
        self.assertEqual(self.robot.get_wheel_speeds(), (1, 2))
        self.robot.arc_right(2, .5)
        self.assertEqual(self.robot.get_wheel_speeds(), (2, 1))
        with self.assertRaises(ValueError): self.robot.arc_left(2, -1)
    def test_13_timed_motion_stops(self):
        self.assertTrue(self.robot.move_for(.1, 1, 2))
        self.assertGreaterEqual(self.robot.time(), .1)
        self.assertEqual(self.robot.get_wheel_speeds(), (0, 0))
    def test_14_zero_timed_motion(self):
        self.assertTrue(self.robot.move_for(0, 1, 1))
        self.assertEqual(self.robot.time(), 0)
    def test_15_invalid_timed_motion(self):
        with self.assertRaises(ValueError): self.robot.move_for(-1, 1, 1)
    def test_16_timed_directions(self):
        self.assertTrue(self.robot.forward_for(.07, safe=False))
        self.assertTrue(self.robot.backward_for(.07))
        self.assertTrue(self.robot.turn_left_for(.07))
        self.assertTrue(self.robot.turn_right_for(.07))
        self.assertEqual(self.robot.get_wheel_speeds(), (0, 0))
    def test_17_sensor_range(self):
        self.backend.by_name['so3'].value = 1024
        self.assertAlmostEqual(self.robot.sonar_raw(3), 1024)
        self.assertAlmostEqual(self.robot.sonar_distance(3), 0)
        self.backend.by_name['so3'].value = 512
        self.assertAlmostEqual(self.robot.sonar_distance(3), 2.5)
        self.backend.by_name['so3'].value = 0
        self.assertAlmostEqual(self.robot.sonar_distance(3), 5)
    def test_18_sonar_errors(self):
        with self.assertRaises(ValueError): self.robot.sonar_raw(16)
        with self.assertRaises(ValueError): self.robot.minimum_distance([])
    def test_19_distance_groups(self):
        self.assertEqual(len(self.robot.read_all_sonars()), 16)
        self.assertAlmostEqual(self.robot.front_distance(), 5)
        self.assertAlmostEqual(self.robot.left_distance(), 5)
        self.assertAlmostEqual(self.robot.right_distance(), 5)
        self.assertAlmostEqual(self.robot.rear_distance(), 5)
        self.assertAlmostEqual(self.robot.minimum_distance([1, 2]), 5)
    def test_20_obstacle_directions(self):
        self.backend.by_name['so3'].value = 1000
        self.assertTrue(self.robot.obstacle_ahead(.5))
        self.assertTrue(self.robot.obstacle_left(.5))
        self.assertFalse(self.robot.obstacle_right(.5))
        self.backend.by_name['so4'].value = 1000
        self.assertTrue(self.robot.obstacle_right(.5))
    def test_21_obstacle_threshold_errors(self):
        with self.assertRaises(ValueError): self.robot.obstacle_ahead(0)
    def test_22_safe_motion_blocked(self):
        self.backend.by_name['so3'].value = 1024
        self.assertFalse(self.robot.forward_for(.4, safe=True))
        self.assertEqual(self.robot.get_wheel_speeds(), (0, 0))
        self.assertEqual(self.robot.time(), 0)
    def test_23_encoder(self):
        position = self.robot.read_wheel_encoders()
        self.assertEqual(len(position), 4)
        self.assertTrue(all(v == 1 for v in position.values()))
    def test_24_no_camera(self):
        with self.assertRaises(CameraNotAvailableError): self.robot.capture_frame()
        with self.assertRaises(CameraNotAvailableError): self.robot.camera_resolution()
    def test_25_camera_available(self):
        robot = RoboStart(backend=FakeRobot(camera=True))
        self.assertTrue(robot.camera_available)
        self.assertEqual(robot.camera_resolution(), (4, 2))
        robot.close()
    def test_26_sim_termination(self):
        robot = RoboStart(backend=FakeRobot(stop_after=1))
        self.assertTrue(robot.step())
        self.assertFalse(robot.step())
        self.assertFalse(robot.step())
        robot.close()
    def test_27_timed_termination_stop(self):
        robot = RoboStart(backend=FakeRobot(stop_after=2))
        self.assertFalse(robot.forward_for(1, safe=False))
        self.assertEqual(robot.get_wheel_speeds(), (0, 0))
        robot.close()
    def test_28_context_manager(self):
        with RoboStart(backend=FakeRobot()) as robot:
            robot.forward()
        self.assertEqual(robot.get_wheel_speeds(), (0, 0))
    def test_29_missing_motor(self):
        backend = FakeRobot()
        backend.items = [x for x in backend.items if x.getName() != 'front left wheel']
        with self.assertRaises(DeviceNotFoundError): RoboStart(backend=backend)
    def test_30_missing_sonar(self):
        backend = FakeRobot()
        backend.items = [x for x in backend.items if x.getName() != 'so8']
        with self.assertRaises(DeviceNotFoundError): RoboStart(backend=backend)
    def test_31_no_encoders(self):
        backend = FakeRobot()
        backend.items = [x for x in backend.items if not x.getName().endswith('sensor')]
        robot = RoboStart(backend=backend)
        with self.assertRaises(DeviceNotFoundError): robot.read_wheel_encoders()
        robot.close()


if __name__ == '__main__':
    unittest.main()
