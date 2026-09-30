import pygame as pg

class Scrollbar:
    def __init__(self, size:tuple[float,float], backgroundColor, floaterHeight:float, floaterSprite:pg.Surface):
        self.size = size
        self.backgroundCol = backgroundColor
        self.floaterSprite = floaterSprite

        self.rect = pg.Rect(
            0,
            0,
            self.size[0],
            self.size[1]
        )

        self.floaterRect = pg.Rect(
            0,
            0,
            self.size[0],
            floaterHeight
        )

        self.render_surface = pg.Surface(self.size)

    def _render(self):
        # background
        self.render_surface.fill(self.backgroundCol)

        # floater
        self.render_surface.blit(self.floaterSprite, self.floaterRect)

    def _set_scroll_pos(self, pos:float): # <0-1>
        self.floaterRect.y = pos * self.size[1]

    def get_scroll_pos(self): # <0-1>
        return self.floaterRect.y / self.size[1]

    def get_surface(self, update:bool=True):

        if update:
            self._render()

        return self.render_surface