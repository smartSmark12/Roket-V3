import pygame as pg

from game.scripts.sprite_window import SpriteWindow
from scripts.colors import *

max_title_length = 17

class ShipModInteractiveSlot:
    def __init__(self, appInstance, rect:pg.Rect, icon:pg.Surface, iconTop:pg.Surface|None, title:str, slotID:int):
        self.app = appInstance
        self.rect = rect
        self.icon = self.app.sprite_handler.rescale_sprite(icon, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))
        self.iconTop = self.app.sprite_handler.rescale_sprite(iconTop, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))
        self.title = title

        self.slotID = slotID

        self.corrected_rect = pg.Rect(
            self.app.to_scale((self.rect.x, self.rect.y)),
            self.app.to_scale((self.rect.width, self.rect.height))
        )

        self.hovered = False
        self.clicked = False

    def render(self):
        # background
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_very_light_blue})
        self.app.draw("rect", self.app.LAYER_UI_TOP, {"rect":self.corrected_rect, "color":roket_yellow, "width":self.app.to_scale_x(8)})

        # icon
        self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.icon, "rect":self.corrected_rect})
        if self.iconTop != None:
            self.app.draw("sprite", self.app.LAYER_UI_TOP, {"sprite":self.iconTop, "rect":self.corrected_rect})

        # text
        self.app.draw("text", self.app.LAYER_UI_TOP, {"text":self.title[:max_title_length], "rect":pg.Rect(self.app.to_scale((self.rect.x + self.rect.height + 5, self.rect.y + 10)), self.app.to_scale((self.rect.width, self.rect.height))), "color":roket_dark_blue, "font":self.app.ship_mod_slot_font, "no_bg":True})

    def get_slot_id(self):
        return self.slotID

    def activation_detection(self):
        if self.rect.collidepoint(self.app.corrected_mouse_info[0]):
            self.hovered = True

            if self.app.corrected_mouse_info[1] and self.app.corrected_mouse_info[2]:
                self.clicked = True

                return True

            else:
                self.clicked = False

            return False

        else:
            self.hovered = False
            self.clicked = False

            return False