import pygame as pg

from game.scripts.scenes.intermediate_scene         import IntermediateScene
from game.scripts.scenes.global_scene_params        import GlobalSceneParams as gs

from scripts.core.settings                          import GAME_VERSION, GAME_VERSION_HINT, WIDTH, HEIGHT
from vuilib.vui_flatpane                            import flatpane
from vuilib.vui_button                              import button
from game.scripts.vuilib_extension.text_button      import TextButton
from functools                                      import partial

class TitleScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "title")

        self.main_text = self.app.texts["title_title"]
        self.version_text = "v" + GAME_VERSION + " - " + GAME_VERSION_HINT
        self.play_text = self.app.texts["title_play"] + " " + self.app.get_keybind_keycode_name_in_square_brackets("ui_forward")
        self.exit_text = self.app.texts["title_exit"] + " " + self.app.get_keybind_keycode_name_in_square_brackets("ui_back")
        self.buttons = {}
        self.planets = []

        ## create all title buttons
        self.buttons["play"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.title_button_width) / 2), self.to_scale_y((HEIGHT - gs.title_button_height) / 2 + gs.title_button_y_offset), self.to_scale_x(gs.title_button_width), self.to_scale_y(gs.title_button_height)),
            0,
            None,
            partial(self.scene_handler.setActiveScene, "main_menu"),
            None,
            self.app,
            self.play_text
        )
        
        self.buttons["exit"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.title_button_width) / 2), self.to_scale_y((HEIGHT - gs.title_button_height) / 2 + 2 * gs.title_button_y_offset), self.to_scale_x(gs.title_button_width), self.to_scale_y(gs.title_button_height)),
            0,
            None,
            partial(self.app.exit_game),
            None,
            self.app,
            self.exit_text
        )
        
        self.buttons["settings"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["mainmenu_settings_button"], "hover":self.sprites["mainmenu_settings_button_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.title_square_button_size) / 2 - gs.title_side_button_x_distance), self.to_scale_y((HEIGHT - gs.title_square_button_size) / 2 + gs.title_button_y_offset), self.to_scale_x(gs.title_square_button_size), self.to_scale_y(gs.title_square_button_size)),
            0,
            None,
            partial(self.app.show_info_popup, "options pressed"),
            None,
            self.app
        )

        self.buttons["achievements"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["mainmenu_leaderboard_button"], "hover":self.sprites["mainmenu_leaderboard_button_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.title_square_button_size) / 2 + gs.title_side_button_x_distance), self.to_scale_y((HEIGHT - gs.title_square_button_size) / 2 + gs.title_button_y_offset), self.to_scale_x(gs.title_square_button_size), self.to_scale_y(gs.title_square_button_size)),
            0,
            None,
            partial(self.app.show_warning_popup, "achievements pressed"),
            None,
            self.app
        )

        