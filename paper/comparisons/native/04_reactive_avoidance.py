from controller import Robot
robot = Robot()
dt = int(robot.getBasicTimeStep())
left_names = ("front left wheel", "back left wheel")
right_names = ("front right wheel", "back right wheel")
left = [robot.getDevice(x) for x in left_names]
right = [robot.getDevice(x) for x in right_names]
for motor in left + right:
    motor.setPosition(float("inf"))
    motor.setVelocity(0.0)
sonars = [robot.getDevice(f"so{i}") for i in (2, 3, 4, 5)]
for sonar in sonars:
    sonar.enable(dt)
for _ in range(35):
    distances = [5.0 * (1.0 - max(0.0, min(1024.0, s.getValue())) / 1024.0) for s in sonars]
    obstacle = min(distances) < 0.65
    for motor in left:
        motor.setVelocity(-1.4 if obstacle else 1.5)
    for motor in right:
        motor.setVelocity(1.4 if obstacle else 1.5)
    if robot.step(dt) == -1:
        break
for motor in left + right:
    motor.setVelocity(0.0)
