class Alarm:
    def __init__(self, name:str, timeout:int|float, timeoutFunction, repeat:bool):
        self.name = name
        self.timeout = timeout
        self.function = timeoutFunction
        self.repeat = repeat

        self.time = 0
        self.scheduledToRemove = False

        self.paused = False

    def checkTimeout(self, deltaTime:float) -> bool:
        if not self.getPaused():
            self.time += deltaTime

            if self.time >= self.timeout:
                self.trigger()

                self.time -= self.timeout

                return True

            else:
                return False

    def getRepeat(self):
        return self.repeat

    def trigger(self):
        try:
            self.function()
        except Exception as e:
            print(f"{__name__}: alarm {self.name} failed to trigger timeout function ({e})")

    def pauseAlarm(self):
        self.paused = True

    def unpauseAlarm(self):
        self.paused = False

    def getPaused(self):
        return self.paused

    def removeAlarm(self):
        self.scheduledToRemove = True

    def getRemoveSchedule(self):
        return self.scheduledToRemove