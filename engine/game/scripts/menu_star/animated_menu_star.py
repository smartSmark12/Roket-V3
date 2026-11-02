from pygame import Rect

from game.scripts.menu_star.menu_star       import MenuStar
from scripts.vanimlib.val_animatedTexture   import AnimatedTexture

class AnimatedMenuStar(MenuStar): # you see, it inherits, but only in spirit. Its like the ship of Theseus
    def __init__(self, appInstance, pos:tuple, speed:tuple, size:float|int, rotation:float|int, rotSpeed:float|int, animatedTextureName:str):
        self.app                            = appInstance
        self.pos                            = pos
        self.speed                          = speed
        self.size                           = size
        self.rotation                       = rotation
        self.rotationSpeed                  = rotSpeed
        self.animatedSpriteName             = animatedTextureName
        self.animatedSprite:AnimatedTexture = self.app.animations[self.animatedSpriteName]

    def update(self):
        self.pos = (
            self.pos[0] + self.speed[0] * self.app.dt,
            self.pos[1] + self.speed[1] * self.app.dt
        )

        self.sprite = self.app.sprite_handler.cached_real_scale_sprite(
            self.animatedSprite.sprite,
            (self.size, self.size)
        )

        self.rotation += self.rotationSpeed * self.app.dt

    def render(self):

        sprite = self.app.sprite_handler.rotate(
                self.sprite,
                int(self.rotation)
            ) # int safety check

        self.app.draw(
            "sprite",
            self.app.LAYER_TITLE_STARS,
            {
                "sprite":sprite,
                "rect":Rect(
                    self.app.to_scale((self.pos[0] - sprite.width / 2, self.pos[1] - sprite.height / 2)),
                    (0,0)
                )
            }
        )