import pygame as pg

from scripts.colors import *

class ShipModInteractiveSlot:
    def __init__(self, appInstance, rect:pg.Rect, icon:pg.Surface):
        self.app = appInstance
        self.rect = rect
        self.icon = self.app.sprite_handler.rescale_sprite(icon, (self.app.to_scale_x(rect.height), self.app.to_scale_y(rect.height)))

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
        
    def activation_detection(self):
        if self.corrected_rect.collidepoint(self.app.corrected_mouse_info[0]):
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