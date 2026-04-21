import pygame as pg
from functools import partial

from scripts.core.settings import POPUP_WINDOW_SIZE, POPUP_WINDOW_TEXT_LENGTH, WIDTH, HEIGHT
from game.scripts.vuilib_extension.text_button import TextButton
from vuilib.vui_flatpane import flatpane
from scripts.colors import *
from game.scripts.ui_frame_builder import UIFrameBuilder

class PopupWindow:
    def __init__(self, appInstance, content:str, actions:list[str]=["OK"]):
        self.app = appInstance
        self.actions = actions

        # create background
        self.background = UIFrameBuilder.get_ui_frame(self.app.to_scale_x(POPUP_WINDOW_SIZE[0]), self.app.to_scale_y(POPUP_WINDOW_SIZE[1]), self.app.sprites, alpha=True)

        self._rect = pg.Rect((0,0),self.app.to_scale((POPUP_WINDOW_SIZE[0],POPUP_WINDOW_SIZE[1]))) # corrected rect, dont use as ref
        self._rect.center = self.app.to_scale((WIDTH / 2, HEIGHT / 2))

        # process content
        self.content:list[str] = self._split_content(content)

        # create buttons
        self.buttons = self._create_buttons(self.actions)

    def _split_content(self, content) -> list[str]:
        contents = [""]
        src_content:list[str] = content.split()

        num_rows = 0

        for item in src_content:
            len_contents = len(contents[num_rows])

            if len_contents + len(item) < POPUP_WINDOW_TEXT_LENGTH:
                contents[num_rows] += item + " "
            else:
                num_rows += 1
                contents.append(item + " ")

        return contents
    
    def _create_buttons(self, actions:list[str]):
        button_margin = 10 # idk anymore
        button_size = (280, 128)
        buttons = []

        num_buttons = len(actions)

        for action_index in range(len(self.actions)):
            action = self.actions[action_index]

            button_rect = pg.Rect(0,0,self.app.to_scale_x(button_size[0]),self.app.to_scale_y(button_size[1])) # FIXED button size !
            button_rect.center = (
                self._rect.centerx - self.app.to_scale_x((num_buttons - 1) * (button_size[0] + button_margin) / 2 - (action_index) * (button_size[0] + button_margin)),
                self._rect.y + self._rect.height - self.app.to_scale_y(button_size[1] - 40)
            )

            created_button = TextButton(
                flatpane(
                    "sprite",
                    {
                        "main":self.app.sprites["button_template"],
                        "hover":self.app.sprites["button_template_dark"]
                    },
                    sprite="main"
                ),
                button_rect,
                0,
                None,
                partial(self.app.hide_active_popup),
                None,
                self.app,
                action,
                self.app.LAYER_POPUP_TOP
            )

            buttons.append(created_button)

        return buttons
    
    def update(self):
        self.update_buttons()

    def update_buttons(self):
        for button in self.buttons:
            button.activation_detection(self.app.corrected_mouse_info)

    def _render_background(self):
        self.app.draw(
            "sprite",
            self.app.LAYER_POPUP_BOTTOM,
            {
                "rect":self._rect,
                "sprite":self.background
            }
        )

    def _render_text(self):
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

    def _render_button(self):
        for button in self.buttons:
            button.render()
        #self.app.draw_button_text(self.action, self.button, self.app.LAYER_POPUP_TEXT)
    
    def render(self):
        # draw background
        self._render_background()

        # draw texts
        self._render_text()

        # draw button
        self._render_button()
        