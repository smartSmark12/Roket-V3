from vuilib.vui_button          import button
from vuilib.vui_flatpane        import flatpane
from game.scripts.sprite_window import SpriteWindow

from scripts.colors             import black

import pygame as pg

class LevelButton(button):
    def __init__(self, flatpane_sprite:flatpane, rect:pg.Rect|tuple, hold_time:int|float, on_hover_function, on_click_function, on_hold_function, appInstance, text:str, icon:pg.Surface, target_surface:pg.Surface, renderLayer:int = None):
        super().__init__(flatpane_sprite, rect, hold_time, on_hover_function, on_click_function, on_hold_function, appInstance, renderLayer)

        self.text = text
        self.icon = icon
        self.target = target_surface

        #self.render_rect = pg.Rect(
        #            self.app.to_scale(self.rect.topleft),
        #            self.app.to_scale(self.rect.size)
        #        )

        icon_offset = self.rect.height / 10

        self.icon_window = SpriteWindow(
            self.app,
            self.icon,
            (self.rect.x + icon_offset, self.rect.y + icon_offset),
            (self.rect.height - 2 * icon_offset, self.rect.height - 2 * icon_offset),
            self.renderLayer + 1,
            external=True
        )

    def render(self):
        render_data = []

        render_data.append(self.app.draw("sprite", self.renderLayer, {"sprite":self.sprite.sprite, "rect":self.rect}, external=True))

        # render icon
        render_data.append(self.icon_window.render())
        #render_data.append(self.app.draw("sprite", self.renderLayer + 1, {"sprite":self.icon, "rect":(self.icon_rect)}, external=True))

        # render text
        render_data.append(self.app.draw("text", self.renderLayer + 1, {"text":self.text, "no_bg":True, "font":self.app.button_font, "center":self.rect.center, "color":black}, external=True)) # gl debugging why the text isnt rendering xd

        return render_data

