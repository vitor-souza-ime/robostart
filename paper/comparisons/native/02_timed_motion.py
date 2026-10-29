from controller import Robot
robot = Robot()
dt = int(robot.getBasicTimeStep())
names = ("front left wheel", "back left wheel", "front right wheel", "back right wheel")
motors = [robot.getDevice(name) for name in names]
for motor in motors:
    motor.setPosition(float("inf"))
    motor.setVelocity(1.5)
target_time = robot.getTime() + 0.5
while robot.getTime() < target_time:
    if robot.step(dt) == -1:
        break
for motor in motors:
    motor.setVelocity(0.0)
