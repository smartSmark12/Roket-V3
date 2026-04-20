import pygame as pg

from game.scripts.ship_modification_related.ship_modification_slot import ShipModInteractiveSlot

from scripts.colors import *
from scripts.core.settings import MOD_SLOT_TITLE_LENGTH

class ShipModInteractiveSlotSlot(ShipModInteractiveSlot):

    def __init__(self, appInstance, rect:pg.Rect, icon:pg.Surface, iconTop:pg.Surface|None, title:str, slotPos:tuple, allowedModTypes:list[str], slotID:int):
        super().__init__(appInstance, rect, icon)

        self.iconTop = self.app.sprite_handler.rescale_sprite(iconTop, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))
        self.title = title

        self.slotPos = slotPos
        self.allowedModTypes = allowedModTypes

        self.slotID = slotID

    def render(self):
        # background
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_very_light_blue})
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_yellow, "width":self.app.to_scale_x(8)})

        # icon
        self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.icon, "rect":self.corrected_rect})
        if self.iconTop != None:
            self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.iconTop, "rect":self.corrected_rect})

        # text
        self.app.draw("text", self.app.LAYER_UI_TOP, {"text":self.title[:MOD_SLOT_TITLE_LENGTH], "rect":pg.Rect(self.app.to_scale((self.rect.x + self.rect.height + 5, self.rect.y + 10)), self.app.to_scale((self.rect.width, self.rect.height))), "color":roket_dark_blue, "font":self.app.ship_mod_slot_font, "no_bg":True})

    def get_slot_id(self):
        return self.slotID