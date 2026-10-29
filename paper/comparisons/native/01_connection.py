from controller import Robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())
print("Connected:", robot.getName())
print("Basic time step (ms):", timestep)
print("Initial simulated time:", robot.getTime())
