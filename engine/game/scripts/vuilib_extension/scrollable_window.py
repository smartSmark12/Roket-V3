import pygame as pg

from game.scripts.vuilib_extension.scrollbar import Scrollbar

class ScrollableWindow:
    def __init__(self, size:tuple[float,float], scrollbar:Scrollbar, backgroundColor=None):
        self.size = size
        self.scrollbar = scrollbar
        self.backgroundCol = backgroundColor

        self.rect = pg.Rect(
            0,
            0,
            self.size[0],
            self.size[1]
        )

        self.render_surface = pg.Surface(
            self.size
        )

        self.get_scroll_pos = self.scrollbar.get_scroll_pos

    def set_scroll_pos(self, pos:float): # <0-1> scroll distance ## update the scrollbar pos too!
        self.scrollbar._set_scroll_pos(pos)

    def set_content(self, contentSprite:pg.Surface): # have to provide a pre_rendered surface to be scrolled
        self.content_sprite = contentSprite

    def _render(self):

        # background
        if self.backgroundCol is not None:
            self.render_surface.fill(self.backgroundCol)

        # content
        self.render_surface.blit(
            self.content_sprite,
            (
                0,
                - self.get_scroll_pos() * self.size[1]
            )
        )

    def get_scroll_offset(self): # <pixels-y> scroll offset for interaction ## dont forget to check if the click is within the scrollable window itself as to not click on invisible objects!
        return self.size[1] * self.get_scroll_pos()

    def get_surface(self, update:bool=True):
        if update:
            self._render()

        return self.render_surface