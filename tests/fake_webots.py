"""Small fake Webots backend for offline contract tests (NOT a physics simulator)."""

class FakeMotor:
    def __init__(self, name):
        self._name = name
        self.position = None
        self.velocity = None
    def getName(self):
        return self._name
    def setPosition(self, value):
        self.position = value
    def setVelocity(self, value):
        self.velocity = value


class FakeSensor:
    def __init__(self, name, value=0.0):
        self._name = name
        self.value = value
        self.enabled = None
    def getName(self):
        return self._name
    def enable(self, timestep):
        self.enabled = timestep
    def getValue(self):
        return self.value


class FakeCamera(FakeSensor):
    def __init__(self):
        super().__init__('camera')
        self.width = 4
        self.height = 2
        self.raw = bytes((0, 20, 100, 255)) * (self.width * self.height)
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getImage(self):
        return self.raw


class FakeRobot:
    def __init__(self, camera=False, stop_after=None):
        self.now = 0.0
        self.timestep = 32
        self.stop_after = stop_after
        self.steps = 0
        self.items = []
        for name in (
            'front left wheel', 'back left wheel',
            'front right wheel', 'back right wheel'
        ):
            self.items.append(FakeMotor(name))
            self.items.append(FakeSensor(name + ' sensor', value=1.0))
        for i in range(16):
            self.items.append(FakeSensor(f'so{i}', value=0.0))
        if camera:
            self.items.append(FakeCamera())
        self.by_name = {item.getName(): item for item in self.items}

    def getName(self):
        return 'Pioneer 3-AT'
    def getBasicTimeStep(self):
        return self.timestep
    def getTime(self):
        return self.now
    def getNumberOfDevices(self):
        return len(self.items)
    def getDeviceByIndex(self, index):
        return self.items[index]
    def step(self, timestep):
        assert timestep == self.timestep
        if self.stop_after is not None and self.steps >= self.stop_after:
            return -1
        self.steps += 1
        self.now += timestep / 1000.0
        return 0
