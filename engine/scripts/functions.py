def moveCoords(old_position:tuple[int|float], offset:tuple[int|float]) -> tuple[int|float]:
        return (old_position[0] + offset[0], old_position[1] + offset[1])

""" def move_toCoords(old_position, position):
    self.position_read = position
    self.destination = (self.position_read[0] * math.cos(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])), self.position_read[1] * math.sin(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])))
    self.angle = math.atan2(self.destination[1] - self.position[1], self.destination[0] - self.position[0]) # tohle chce ještě pořádně prohlédnout """

def move_towards(self, object):
    self.object = object
    self.destination = (self.position_read[0] * math.cos(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])), self.position_read[1] * math.sin(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])))
    self.angle = math.atan2(self.destination[1] - self.position[1], self.destination[0] - self.position[0]) # tohle chce ještě pořádně prohlédnout

def exponential_move(self):
    pass

def move_in_out(self):
    pass