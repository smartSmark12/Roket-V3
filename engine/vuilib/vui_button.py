import pygame as pg
from scripts.colors import *
from vuilib.vui_flatpane import flatpane
""" from scripts.datablock import Datablock """

class button:
    def __init__(self, flatpane_sprite: flatpane, rect: pg.Rect | tuple, hold_time: int | float, on_hover_function, on_click_function, on_hold_function, appInstance):
        self.rect = rect
        self.sprite = flatpane_sprite
        self.hold_time = hold_time
        self.held_for = 0
        self.hover = False
        self.on_hover_function = on_hover_function
        self.on_click_function = on_click_function
        self.on_hold_function = on_hold_function

        self.app = appInstance

        if type(self.rect != pg.Rect):
            try:
                self.rect = pg.Rect(self.rect[0], self.rect[1], self.rect[2], self.rect[3])
            except:
                self.app.ext_append_to_log(f"{__name__}: incorrect Rect type entered for button ({self.rect})")
                self.rect = pg.Rect(100, 100, 100, 100)

    def activation_detection(self, mouse_info: tuple):
        if self.rect.collidepoint(mouse_info[0]):
            self.on_hover()
            self.hover = True
            self.update_hold_time(mouse_info)
            if mouse_info[1] and mouse_info[2]:
                self.on_click()
                if self.held_for > self.hold_time:
                    self.on_hold()

            self.set_active_sprite("hover")

            return True
        else:
            self.hover = False
            self.passive_update()
            
            return False
    
    def update_hold_time(self, mouse_info):
        if mouse_info[1]:
            self.held_for += self.app.dt
        else:
            self.held_for = 0

    def passive_update(self):
        self.set_active_sprite("main")

    def set_active_sprite(self, spriteName:str):
        self.sprite.set_active_sprite(spriteName)

    def render(self):
        self.app.draw("sprite", self.app.LAYER_UI_BOTTOM, {"sprite":self.sprite.sprite, "rect":self.rect})

    def on_hover(self):
        if self.on_hover_function != None:
            self.on_hover_function()

    def on_click(self):
        if self.on_click_function != None:
            self.on_click_function()

    def on_hold(self):
        if self.on_hold_function != None:
            self.on_hold_function()