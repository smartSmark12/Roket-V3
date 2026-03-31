class Page:
    def __init__(self, slots:list):
        self.slots = slots

    def get_slot(self, slotIndex):
        if slotIndex in self.slots:
            return self.slots[slotIndex]
        
    def get_slots(self):
        return self.slots
    
    def clear_slots(self):
        self.slots = []

    def add_slot(self, slotToAdd):
        self.slots.append(slotToAdd)