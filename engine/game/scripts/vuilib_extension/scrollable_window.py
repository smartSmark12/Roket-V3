import pygame as pg

from game.scripts.vuilib_extension.scrollbar import Scrollbar

class ScrollableWindow:
    def __init__(self, appInstance, pos:tuple[float,float], size:tuple[float,float], scrollbar:Scrollbar, backgroundColor=None, layer:int|None=None, scrollSpeedMultiplier:float=1.):
        self.app = appInstance
        self.pos = pos
        self.size = size
        self.scrollbar = scrollbar
        self.backgroundCol = backgroundColor
        self.scrollSpeed = scrollSpeedMultiplier

        self.layer = layer if layer is not None else self.app.LAYER_UI_TOP

        self.rect = pg.Rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1]
        )

        self.render_rect = pg.Rect( # also for mouse collision
            self.app.to_scale_x(self.pos[0]),
            self.app.to_scale_y(self.pos[1]),
            self.app.to_scale_x(self.size[0]),
            self.app.to_scale_y(self.size[1])
        )

        self.render_surface = pg.Surface(
            self.size
        )

        self.content_sprite = None
        self.content_height = 0

        self.get_scroll_pos = self.scrollbar.get_scroll_pos

    def is_scrollable(self):
        return self.content_height > self.size[1]

    def set_scroll_pos(self, pos:float): # <0-1> scroll distance ## update the scrollbar pos too!
        self.scrollbar._set_scroll_pos(pos)

    def set_content(self, contentSprite:pg.Surface): # have to provide a pre_rendered surface to be scrolled
        self.content_sprite = contentSprite

        self.content_height = self.content_sprite.height
        self.scrollbar.set_content_height(self.content_sprite.height)

    def update(self):
        if self.is_scrollable():
            if self.render_rect.collidepoint(self.app.corrected_mouse_info[0]):
                self.set_scroll_pos(self.get_scroll_pos() - (self.app.corrected_mouse_info[3][1] / self.content_height) * self.scrollSpeed)

    def _render(self):

        # background
        if self.backgroundCol is not None:
            self.render_surface.fill(self.backgroundCol)

        # content
        if self.content_sprite:
            self.render_surface.blit(
                self.content_sprite,
                (
                    0,
                    - self.get_scroll_pos() * (self.content_height - self.size[1])
                )
            )

    def render(self):
        self._render()

        # render scrollbar only if the content is longer than the page
        if self.is_scrollable():
            self.scrollbar.render()

        self.app.draw("sprite", self.layer, {"sprite":self.app.sprite_handler.real_scale_sprite(self.render_surface, self.size), "rect":self.render_rect})

    def _get_scroll_offset(self): # <pixels-y> scroll offset for interaction ## dont forget to check if the click is within the scrollable window itself as to not click on invisible objects!
        return self.size[1] * self.get_scroll_pos()

    def get_scroll_corrected_pos(self, pos:tuple[float|float]):
        return (pos[0], pos[1] + self._get_scroll_offset())

    def get_surface(self, update:bool=True):
        if update:
            self._render()

        return self.render_surface