import pygame as pg
from functools import partial

from scripts.core.settings import POPUP_WINDOW_SIZE, POPUP_WINDOW_TEXT_LENGTH, WIDTH, HEIGHT
from vuilib.vui_button import button
from vuilib.vui_flatpane import flatpane
from scripts.colors import *
from game.scripts.ui_frame_builder import UIFrameBuilder

class PopupWindow:
    def __init__(self, appInstance, content:str, action:str="OK"):
        self.app = appInstance
        self.action = action
        self.background = UIFrameBuilder.get_ui_frame(self.app.to_scale_x(POPUP_WINDOW_SIZE[0]), self.app.to_scale_y(POPUP_WINDOW_SIZE[1]), self.app.sprites, alpha=True)

        self._rect = pg.Rect((0,0),self.app.to_scale((POPUP_WINDOW_SIZE[0],POPUP_WINDOW_SIZE[1]))) # corrected rect, dont use as ref
        self._rect.center = self.app.to_scale((WIDTH / 2, HEIGHT / 2))

        self.content:list[str] = self._split_content(content)

        self.button_rect = pg.Rect(0,0,self.app.to_scale_x(280),self.app.to_scale_y(128))
        self.button_rect.center = (
            self._rect.centerx,
            self._rect.y + self._rect.height - self.app.to_scale_y(128 - 40)
        )
        self.button = button(
            flatpane(
                "sprite",
                {
                    "main":self.app.sprites["button_template"],
                    "hover":self.app.sprites["button_template_dark"]
                },
                sprite="main"
            ),
            self.button_rect,
            0,
            None,
            partial(self.app.hide_active_popup),
            None,
            self.app,
            self.app.LAYER_POPUP_TOP
        )

    def _split_content(self, content) -> list[str]:
        contents = []
        src_content = content

        while len(src_content) > 0:
            contents.append(
                src_content[:POPUP_WINDOW_TEXT_LENGTH] # i heckin luv this thing
            )

            src_content = src_content[POPUP_WINDOW_TEXT_LENGTH:]

        return contents
    
    def update_buttons(self):
        self.button.activation_detection(self.app.corrected_mouse_info)
    
    def render(self):
        # draw background
        self.app.draw(
            "sprite",
            self.app.LAYER_POPUP_BOTTOM,
            {
                "rect":self._rect,
                "sprite":self.background
            }
        )

        # draw texts
        for text_index in range(len(self.content)):
            text = self.content[text_index]
            self.app.draw(
                "text",
                self.app.LAYER_POPUP_TEXT,
                {
                    "rect":(0,0,0,0),
                    "text":text,
                    "center":(self._rect.centerx, self._rect.y + self.app.to_scale_y(text_index * 35 + 40)),
                    "font":self.app.ship_mod_slot_font,
                    "color":roket_dark_blue,
                    "no_bg":True
                }
            )

        # draw button
        self.button.render()
        self.app.draw_button_text(self.action, self.button, self.app.LAYER_POPUP_TEXT)