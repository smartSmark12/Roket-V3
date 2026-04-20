from game.scripts.roket_body_related.roket_module_slot import RoketModuleSlot
from engine.game.scripts.ship_modification_related.ship_modification_slot_slot import ShipModInteractiveSlot
from game.scripts.pageable_panel.page import Page

class ShipModPage(Page):
    def __init__(self, moduleSlots:list[ShipModInteractiveSlot]=[]):
        super().__init__(moduleSlots)

    def add_slot(self, slotToAdd:ShipModInteractiveSlot): # more generalised interactiveSlot??
        self.slots.append(slotToAdd)