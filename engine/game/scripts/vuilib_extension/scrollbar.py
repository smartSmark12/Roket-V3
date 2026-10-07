import pygame as pg
import math

from game.scripts.helper import Helper

class Scrollbar:
    def __init__(self, appInstance, pos:tuple[float|float], size:tuple[float,float], windowHeight:float, backgroundColor, floaterHeight:float, floaterSprite:pg.Surface, layer:int|None=None):
        self.app            = appInstance
        self.pos            = pos
        self.size           = size
        self.windowHeight   = windowHeight
        self.backgroundCol  = backgroundColor
        self.floaterSprite  = floaterSprite

        self.layer = layer if layer is not None else self.app.LAYER_UI_TOP

        self.rect = pg.Rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )

        self.render_rect = pg.Rect(
            self.app.to_scale_x(self.pos[0]),
            self.app.to_scale_y(self.pos[1]),
            0,
            0
        )

        self.floaterRect = pg.Rect(
            0,
            0,
            self.size[0],
            floaterHeight
        )

        self.floater_render_rect = pg.Rect(
            0,
            0,
            self.size[0],
            floaterHeight
        )

        self.render_surface = pg.Surface(self.size)

        self.content_height = 0

    def _render(self):
        # background
        self.render_surface.fill(self.backgroundCol)

        # floater
        self.floater_render_rect.y = Helper.remap(self.floaterRect.y, 0, self.size[1], 0, self.size[1] - self.floaterRect.height)

        self.render_surface.blit(self.floaterSprite, self.floater_render_rect)

    def update(self):
        pass # scroll handling

    def render(self):
        self._render()
        self.app.draw("sprite", self.layer, {"sprite":self.app.sprite_handler.real_scale_sprite(self.render_surface, self.size), "rect":self.render_rect})

    def set_content_height(self, height:float):
        self.content_height = height

    def _set_scroll_pos(self, pos:float): # <0-1>
        self.floaterRect.y = Helper.clamp(pos * self.size[1], 0, self.size[1]) # cause python doesnt have a clamp function ofc how smart

    def get_scroll_pos(self): # <0-1>
        return self.floaterRect.y / self.size[1]

    def get_surface(self, update:bool=True):

        if update:
            self._render()

        return self.render_surface