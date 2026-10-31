from pygame import Rect

class MenuStar:
    def __init__(self, appInstance, pos:tuple, speed:tuple, size:float|int, rotation:float|int, rotSpeed:float|int, spriteName:str):
        self.app = appInstance
        self.pos = pos
        self.speed = speed
        self.size = size
        self.rotation = rotation
        self.rotationSpeed = rotSpeed
        self.spriteName = spriteName
        self.sprite =self.app.sprite_handler.real_scale_sprite(
                            self.app.sprites[self.spriteName],
                            (self.size, self.size)
                        )

    def update(self):
        self.pos = (
            self.pos[0] + self.speed[0] * self.app.dt,
            self.pos[1] + self.speed[1] * self.app.dt
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