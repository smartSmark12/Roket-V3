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

class SettingsScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "settings")

        self.buttons = {}

        self.buttons["return"] = DirectionalButton(
            self.app,
            pg.Rect(100, 100, 128, 128),
            False,
            partial(self.scene_handler.setActiveScene, "main_menu")
        )