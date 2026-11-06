import pygame as pg
from game.scripts.helper import Helper

class Slider:
    def __init__(self, appInstance, pos:tuple, size:tuple, floaterSize:float|int, floaterSprite:pg.Surface, backgroundColor:tuple, startingPos:float=0, renderLayer:int=None):
        self.app = appInstance
        self.pos = pos
        self.size = size
        self.rect = pg.Rect(self.pos, self.size)
        self._resolve_orientation()

        self.backgroundColor = backgroundColor

        self.floaterSize = floaterSize
        self.floaterSprite = self.app.sprite_handler.real_scale_sprite(floaterSprite, (floaterSize, floaterSize))

        self.renderLayer = renderLayer if renderLayer is not None else self.app.LAYER_UI_TOP_BOTTOM

        self.sliderPos = 0
        self.set_slider_pos(startingPos)

        self.held = False

    def _resolve_orientation(self): # 0 horizontal, 1 vertical
        self.orientation = self.size[1] > self.size[0]

    def _mouse_to_slider_pos(self, pos:tuple) -> float:
        slider_coords = (
            (pos[0] - self.pos[0]) / self.size[0],
            (pos[1] - self.pos[1]) / self.size[1]
        )

        if not self.orientation:
            return slider_coords[0]
        else:
            return slider_coords[1]

    def move(self, newPos:tuple):
        self.pos = newPos
        self.rect.topleft = newPos

    def set_slider_pos(self, newPos:float):
        self.sliderPos = Helper.clamp(newPos, 0, 1)

    def get_slider_pos(self):
        return self.sliderPos

    def update(self):

        mouse_pos = self.app.unscale(self.app.corrected_mouse_info[0])
        mouse_down = self.app.corrected_mouse_info[1]
        mouse_changed = self.app.corrected_mouse_info[2]

        # check for hold start
        if self.rect.collidepoint(mouse_pos): # hovered
            if mouse_down and mouse_changed: # started holding
                self.held = True
                self.app.set_mouse_busy(True)

        # check for hold end and update pos
        if self.held:
            if not mouse_down:
                self.held = False
                self.app.set_mouse_busy(False)

            self.set_slider_pos(self._mouse_to_slider_pos(mouse_pos))

    def render(self):
        # draw background
        self.app.draw(
            "rect",
            self.renderLayer,
            {
                "rect":(
                    self.app.to_scale(self.pos),
                    self.app.to_scale(self.size)
                ),
                "color":self.backgroundColor
            }
        )

        # draw floater
        self.app.draw(
            "sprite",
            self.renderLayer,
            {
                "rect":(
                    self.app.to_scale_x((self.pos[0] + self.sliderPos * self.size[0]) if not self.orientation else (self.pos[0] + self.size[0] / 2)) - self.floaterSprite.width / 2,
                    self.app.to_scale_y((self.pos[1] + self.sliderPos * self.size[1]) if self.orientation else (self.pos[1] + self.size[1] / 2)) - self.floaterSprite.height / 2,
                    0,
                    0
                ),
                "sprite":self.floaterSprite
            }
        )