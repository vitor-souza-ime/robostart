from controller import Robot
robot = Robot()
dt = int(robot.getBasicTimeStep())
sonars = [robot.getDevice(f"so{i}") for i in (2, 3, 4, 5)]
for sonar in sonars:
    sonar.enable(dt)
if robot.step(dt) != -1:
    readings = [5.0 * (1.0 - max(0.0, min(1024.0, s.getValue())) / 1024.0) for s in sonars]
    print("Front clearance:", round(min(readings), 2), "m")
