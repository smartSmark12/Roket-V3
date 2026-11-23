import pygame as pg

from game.scripts.scenes.intermediate_scene             import IntermediateScene
from game.scripts.scenes.global_scene_params            import GlobalSceneParams as gs

from scripts.core.settings                              import GAME_VERSION, GAME_VERSION_HINT, WIDTH, HEIGHT
from scripts.colors                                     import *
from vuilib.vui_flatpane                                import flatpane
from vuilib.vui_button                                  import button
from game.scripts.vuilib_extension.text_button          import TextButton
from game.scripts.vuilib_extension.directional_button   import DirectionalButton
from game.scripts.vuilib_extension.slider               import Slider
from functools                                          import partial

class GameScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "game")

        self.buttons = {}

        self.buttons["return"] = DirectionalButton(
            self.app,
            pg.Rect(100, 100, gs.title_square_button_size, gs.title_square_button_size),
            False,
            partial(self.scene_handler.setActiveScene, "main_menu")
        )

        self.time_display = 0