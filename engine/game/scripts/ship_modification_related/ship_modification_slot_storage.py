import pygame as pg

from game.scripts.ship_modification_related.ship_modification_slot      import ShipModInteractiveSlot
from game.scripts.modloader.roket_body_related.roket_module             import RoketModule

from scripts.colors                             import *

class ShipModInteractiveSlotStorage(ShipModInteractiveSlot):
    def __init__(self, appInstance, rect:pg.Rect, icon:pg.Surface, iconTop:pg.Surface|None, title:str, paramTexts:list[str], module:RoketModule):
        super().__init__(appInstance, rect, icon)

        self.title = title
        self.texts = paramTexts

        self.iconTop = self.app.sprite_handler.rescale_sprite(iconTop, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))

        self.module = module

    def get_module(self):
        return self.module

    def render(self):
        # background
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_very_light_blue})
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_yellow, "width":self.app.to_scale_x(8)})

        # icon
        self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.icon, "rect":self.corrected_rect})
        if self.iconTop != None:
            self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.iconTop, "rect":self.corrected_rect})

        # mouse hover window
        if self.hovered:
            hover_rect = pg.Rect(self.app.corrected_mouse_info[0], self.app.to_scale((400,300)))

            self.app.draw("rect", self.app.LAYER_UI_TOP_BOTTOM, {"rect":hover_rect, "color":roket_very_light_blue})
            self.app.draw("rect", self.app.LAYER_UI_TOP_BOTTOM, {"rect":hover_rect, "color":roket_yellow, "width":self.app.to_scale_x(8)})

            # hover content
            self.app.draw("text", self.app.LAYER_UI_TOP_TOP, {"text":self.title, "rect":pg.Rect(0,0,0,0), "color":roket_dark_blue, "font":self.app.ship_mod_slot_font, "center":(hover_rect.centerx, hover_rect.y + self.app.to_scale_y(30)), "no_bg":True})