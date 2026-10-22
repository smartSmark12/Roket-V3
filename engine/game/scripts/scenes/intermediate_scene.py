from scripts.core.scenes.scene                      import Scene

class IntermediateScene(Scene):
    def __init__(self, appInstance, name):
        super().__init__(appInstance, name)

        self.sprites            = self.app.sprites
        self.draw               = self.app.draw

        self.to_scale           = self.app.to_scale
        self.to_scale_x         = self.app.to_scale_x
        self.to_scale_y         = self.app.to_scale_y

        self.texts              = self.app.texts
        self.scene_handler      = self.app.scene_handler
        self.sprite_handler     = self.app.sprite_handler