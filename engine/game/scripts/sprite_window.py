import pygame as pg

class SpriteWindow:
    def __init__(self, appInstance, sprite:pg.Surface, pos:tuple[int|float], size:tuple[int|float], renderLayer:int, rescaleSprite:bool=True):
        self.app = appInstance
        self.sourceSprite = sprite
        self.sprite = None # created later
        self.pos = pos
        self.width = size[0]
        self.height = size[1]
        self.layer = renderLayer

        self._rescale_sprite()

    def _rescale_sprite(self):
        self.sprite = pg.transform.scale(self.sourceSprite, (self.app.to_scale_x(self.width), self.app.to_scale_y(self.height)))

    def set_sprite(self, sprite:pg.Surface):
        self.sprite = sprite

    def set_pos(self, pos:tuple[int|float]):
        self.pos = pos

    def set_size(self, size:tuple[int|float], rescaleSprite:bool=True):
        self.width = size[0]
        self.height = size[1]

        if rescaleSprite: self._rescale_sprite()

    def render(self, renderLayer:int|None=None):
        if not renderLayer: renderLayer = self.layer
        self.app.draw("sprite", renderLayer, {"sprite":self.sprite, "rect":(self.app.to_scale_x(self.pos[0]), self.app.to_scale_y(self.pos[1]), self.width, self.height)})