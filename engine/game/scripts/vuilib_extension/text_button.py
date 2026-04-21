from vuilib.vui_button import button
from vuilib.vui_flatpane import flatpane

from scripts.colors import black

import pygame as pg

class TextButton(button):
    def __init__(self, flatpane_sprite:flatpane, rect:pg.Rect|tuple, hold_time:int|float, on_hover_function, on_click_function, on_hold_function, appInstance, text, renderLayer:int = None):
        super().__init__(flatpane_sprite, rect, hold_time, on_hover_function, on_click_function, on_hold_function, appInstance, renderLayer)

        self.text = text

    def render(self):
        super().render()

        # render text
        self.app.draw("text", self.renderLayer + 1, {"text":self.text, "no_bg":True, "font":self.app.button_font, "center":self.rect.center, "color":black}) # gl debugging why the text isnt rendering xd
