# RoboStart 0.1 — Introductory Robotics and Computer Vision Education

A lightweight Python educational wrapper for **Webots Pioneer 3-AT** that
students can execute from **Visual Studio Code (F5)**. Features wheel motion,
simulation-time commands, sixteen sonar sensors, wheel encoders, an optional
RGB camera, and optional object detection with **Ultralytics YOLO11**.

**Status:** experimental/research prototype. The project includes 70 incremental
exercises and offline unit tests. It has *not* yet been validated on the
user's specific Webots world or in an educational study.

## Quick start (Windows)

1. Unzip and open the **RoboStart_v0_1** folder as the VS Code workspace.
2. In your existing Webots world, set `Pioneer3at.controller` to `<extern>`.
3. Save and Play the Webots simulation.
4. Open `examples/01_connection.py` in VS Code.
5. Choose **RoboStart - Run active example (F5)** under Run and Debug and press
   **F5**. Do not use `Run Python File` (it bypasses the Webots launcher).
6. Try `02_robot_info.py`, `05_wait.py`, and `20_timed_forward.py`.
7. For each movement test, **reset and replay the world** to restore the robot
   to its initial position and stop the previous controller process first.

The included `.vscode/run_webots.ps1` assumes Webots is installed at
`C:\Program Files\Webots`, but respects an existing `WEBOTS_HOME` environment
variable. It also adds the current project to `PYTHONPATH`, so an editable
`pip install` is not necessary for F5.

## Install vision dependencies later

```powershell
py -3.12 -m pip install -r requirements-vision.txt
```

Ensure the installed packages are visible to the interpreter configured for
Webots, not just another Python environment. For camera setup see
[`docs/CAMERA_SETUP.md`](docs/CAMERA_SETUP.md). A pretrained YOLO11 nano model
(`yolo11n.pt`) may download on its first use; it is not distributed here.

## Example progression

| Range | Topic | External dependencies |
|---|---|---|
| 01–09 | Webots connection and simulation timers | None |
| 10–29 | Wheel commands, arcs, timed movement | None |
| 30–44 | Sonars, obstacle reactions, encoders, CSV | None |
| 45–49 | Camera capture, resolution, save, preview | Camera; NumPy/OpenCV as needed |
| 50–60 | YOLO detection, filtering, bounding boxes | Camera + Ultralytics |
| 61–66 | Integrated perception and motion | Camera + Ultralytics |
| 67 | Close OpenCV preview explicitly | Camera + OpenCV |
| 68 | Basic API self-check | None |
| 69 | Direct YOLO model loading | Camera + Ultralytics |
| 70 | Explicit cleanup | None |

The complete exercise listing is available in `examples/INDEX.csv`. A
per-function coverage guide is in `docs/FUNCTION_COVERAGE.csv`.

**Examples are separate programs:** run one per F5 invocation. The optional
examples print `SKIPPED` when the camera or YOLO packages are missing; they do
not imply successful execution of those features.

## Core example

```python
from robostart import RoboStart

with RoboStart() as robot:
    robot.forward_for(0.5, speed=1.5, safe=True)
    robot.start_timer("lesson")
    robot.wait(0.3)
    print("Elapsed simulated time:", robot.timer_elapsed("lesson"))
    print("Front clearance (m):", robot.front_distance())
```

## YOLO example (camera required)

```python
from robostart import RoboStart

with RoboStart() as robot:
    robot.load_yolo("yolo11n.pt")
    if robot.step():
        detections = robot.detect_objects(confidence=0.35, image_size=320)
        print(detections)
        if robot.object_detected("person"):
            robot.stop()
```

Each detection has `label`, `confidence`, and `box` fields. Bounding boxes are
reported in image pixels. A COCO-pretrained YOLO model does not necessarily
recognize generic simulation cubes. Sonars and vision are **different** sensors;
use sonars for obstacle clearance and YOLO for object recognition.

## Units and safety

- Wheel velocities are **radians per second**, not linear m/s; the maximum
  commanded magnitude is clamped to 6.4 rad/s for the standard Pioneer PROTO.
- `wait`, timers and timed movement use **Webots simulation seconds**, not
  `time.sleep()` and not wall-clock time.
- `sonar_distance` calculates **approximate metres** from the official PROTO's
  simplified lookup table (0 m -> raw 1024; 5 m -> raw 0).
- YOLO processing latency (`last_inference_ms`) uses **wall-clock** timing.
- The safety-related methods are *demonstrative educational features* and not
  validated collision-avoidance controls for physical robots.

## Offline contract tests

```bash
python -m unittest discover -s tests -v
```

These test the library against fake Webots devices; real Webots integration
must be tested separately. Use `docs/RESEARCH_PLAN.md` for an evaluation plan
and `docs/GUIA_RAPIDO_PT_BR.md` for instructions in Portuguese.

## Dependencies and licensing

RoboStart source is MIT licensed (see LICENSE). Webots and Ultralytics have
independent licenses; check their terms before distributing derivatives or
commercial software. No Webots robot assets or YOLO model weights are bundled.

Official references:

- Webots external controllers: https://cyberbotics.com/doc/guide/running-extern-robot-controllers
- Pioneer3at PROTO: https://github.com/cyberbotics/webots/blob/released/projects/robots/adept/pioneer3/protos/Pioneer3at.proto
- Pioneer sonar PROTO: https://github.com/cyberbotics/webots/blob/released/projects/robots/adept/pioneer3/protos/Pioneer3DistanceSensor.proto
- Ultralytics usage and licensing: https://docs.ultralytics.com/
