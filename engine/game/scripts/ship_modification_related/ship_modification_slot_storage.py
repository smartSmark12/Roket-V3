import pygame as pg

from game.scripts.ship_modification_related.ship_modification_slot import ShipModInteractiveSlot

from scripts.colors import *

class ShipModInteractiveSlotStorage(ShipModInteractiveSlot):
    def __init__(self, appInstance, rect:pg.Rect, icon:pg.Surface, iconTop:pg.Surface|None):
        super().__init__(appInstance, rect, icon)

        self.iconTop = self.app.sprite_handler.rescale_sprite(iconTop, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))

    def render(self):
        # background
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_very_light_blue})
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_yellow, "width":self.app.to_scale_x(8)})

        # icon
        self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.icon, "rect":self.corrected_rect})
        if self.iconTop != None:
            self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.iconTop, "rect":self.corrected_rect})