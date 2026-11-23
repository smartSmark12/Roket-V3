import pygame as pg

from game.scripts.vuilib_extension.text_button import TextButton
from vuilib.vui_flatpane import flatpane

class DirectionalButton(TextButton):
    def __init__(self, appInstance, rect:pg.Rect, direction:bool, on_click_function, renderLayer:int|None = None):
        self.app = appInstance
        self.direction = direction

        sprite = flatpane(
            "sprite",
            {
                "main":self.app.sprites["button_template_square"],
                "hover":self.app.sprites["button_template_square_dark"]
            },
            sprite="main"
        )

        text = "<" if not direction else ">"

        super().__init__(sprite, rect, 0, None, on_click_function, None, appInstance, text, renderLayer)