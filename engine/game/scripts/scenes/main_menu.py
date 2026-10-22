import pygame as pg

from game.scripts.scenes.intermediate_scene         import IntermediateScene
from game.scripts.scenes.global_scene_params        import GlobalSceneParams as gs

from scripts.core.settings                          import GAME_VERSION, GAME_VERSION_HINT, WIDTH, HEIGHT
from vuilib.vui_flatpane                            import flatpane
from vuilib.vui_button                              import button
from game.scripts.vuilib_extension.text_button      import TextButton
from functools                                      import partial
from game.scripts.ui_frame_builder                  import UIFrameBuilder
from game.scripts.sprite_window                     import SpriteWindow

class MainMenuScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "main_menu")

        self.launch_text = self.texts["main_menu_launch"] + " " + self.app.get_keybind_keycode_name_in_square_brackets("ui_forward")
        self.return_text = self.texts["main_menu_return"] + " " + self.app.get_keybind_keycode_name_in_square_brackets("ui_back")

        self.background_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(gs.main_menu_background_frame_width), self.to_scale_y(gs.main_menu_background_frame_height), self.sprites)
        self.background_frame_pos = (gs.main_menu_background_frame_x, gs.main_menu_background_frame_y)
        
        self.ship_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(gs.main_menu_ship_frame_width), self.to_scale_y(gs.main_menu_background_frame_height), self.sprites)
        self.ship_frame_pos = (gs.main_menu_ship_frame_x, gs.main_menu_background_frame_y)
        
        self.mode_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(gs.main_menu_mode_frame_width), self.to_scale_y(gs.main_menu_background_frame_height), self.sprites)
        self.mode_frame_pos = (gs.main_menu_mode_frame_x, gs.main_menu_background_frame_y)
        
        self.news_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(gs.main_menu_news_frame_width), self.to_scale_y(gs.main_menu_background_frame_height), self.sprites)
        self.news_frame_pos = (gs.main_menu_news_frame_x, gs.main_menu_background_frame_y)
        
        self.buttons = {}

        self.buttons["launch"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.main_menu_button_width) / 2), self.to_scale_y(gs.main_menu_button_start_y), self.to_scale_x(gs.main_menu_button_width), self.to_scale_y(gs.main_menu_button_height)),
            0,
            None,
            partial(self.app.launch_from_main_menu),
            None,
            self.app,
            self.launch_text
        )

        self.buttons["return"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale_x((WIDTH - gs.main_menu_button_width) / 2), self.to_scale_y(gs.main_menu_button_start_y + gs.main_menu_button_y_offset), self.to_scale_x(gs.main_menu_button_width), self.to_scale_y(gs.main_menu_button_height)),
            0,
            None,
            partial(self.scene_handler.setActiveScene, "title"),
            None,
            self.app,
            self.return_text
        )
        
        self.ship_window = SpriteWindow(self.app, self.app.get_active_ship().sprites.get_sprite(0), gs.ship_window_pos, gs.ship_window_size, self.app.LAYER_UI_TOP)

        self.buttons["ship_switch_left"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_vertical"], "hover":self.sprites["button_template_vertical_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale(gs.ship_switch_left_button_pos), self.to_scale(gs.ship_switch_size)),
            0,
            None,
            partial(self.app.cycle_main_menu_ship, direction=0),
            None,
            self.app,
            self.texts["main_menu_switch_left"]
        )
        
        self.buttons["ship_switch_right"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_vertical"], "hover":self.sprites["button_template_vertical_dark"]},
                sprite="main"
            ), 
            pg.Rect(self.to_scale(gs.ship_switch_right_button_pos), self.to_scale(gs.ship_switch_size)),
            0,
            None,
            partial(self.app.cycle_main_menu_ship, direction=1),
            None,
            self.app,
            self.texts["main_menu_switch_right"]
        )
        
        self.buttons["ship_modification"] = TextButton(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale(gs.ship_mod_button_pos), self.to_scale(gs.ship_mod_button_size)),
            0,
            None,
            partial(self.scene_handler.setActiveScene, "ship_modification"),
            None,
            self.app,
            self.texts["main_menu_ship_modification"]
        )

        self.ship_name_text = self.app.get_active_ship().get_property("displayName")
        self.ship_name_text_center = (gs.main_menu_ship_frame_x + gs.main_menu_ship_frame_width / 2, gs.main_menu_background_frame_y + 50)

        ### gamemode frame
        self.mode_texts = {}
        self.mode_texts["mode_career"] = self.texts["main_menu_mode_career"]
        self.mode_texts["mode_infinite"] = self.texts["main_menu_mode_infinite"]
        self.mode_texts["mode_dummy"] = self.texts["main_menu_mode_dummy"]
        
        self.buttons["mode_career"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_mode_career_baw"], "hover":self.sprites["button_mode_career"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale(gs.mode_button_start_pos), self.to_scale(gs.mode_button_size)),
            0,
            None,
            partial(self.app.change_gamemode, "mode_career"),
            None,
            self.app
        )
        
        self.buttons["mode_infinite"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_mode_infinite_baw"], "hover":self.sprites["button_mode_infinite"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((gs.mode_button_start_pos[0], gs.mode_button_start_pos[1] + gs.mode_button_size[1] + gs.mode_button_margin)), self.to_scale(gs.mode_button_size)),
            0,
            None,
            partial(self.app.change_gamemode, "mode_infinite"),
            None,
            self.app
        )
        
        self.buttons["mode_dummy"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_mode_dummy_baw"],
                "hover":self.sprites["button_mode_dummy"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((gs.mode_button_start_pos[0], gs.mode_button_start_pos[1] + 2 * gs.mode_button_size[1] + 2 * gs.mode_button_margin)), self.to_scale(gs.mode_button_size)),
            0,
            None,
            partial(self.app.change_gamemode, "mode_dummy"),
            None,
            self.app
        )

        self.mode_button_names = ["mode_career", "mode_infinite", "mode_dummy"]

  