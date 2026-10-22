import pygame as pg

from game.scripts.scenes.intermediate_scene                             import IntermediateScene
from game.scripts.scenes.global_scene_params                            import GlobalSceneParams as gs

from scripts.core.settings                                              import GAME_VERSION, GAME_VERSION_HINT, WIDTH, HEIGHT, BUTTON_COLOR_SUBTRACT_COLOR
from vuilib.vui_flatpane                                                import flatpane
from vuilib.vui_button                                                  import button
from game.scripts.vuilib_extension.text_button                          import TextButton
from functools                                                          import partial
from game.scripts.ui_frame_builder                                      import UIFrameBuilder
from game.scripts.sprite_window                                         import SpriteWindow
from game.scripts.vuilib_extension.scrollbar                            import Scrollbar
from game.scripts.vuilib_extension.scrollable_window                    import ScrollableWindow
from scripts.colors                                                     import *

class CareerScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "career")

        self.buttons = {}

        self.background_frame = UIFrameBuilder.get_ui_frame(
            self.to_scale_x(gs.career_background_frame_size[0]),
            self.to_scale_y(gs.career_background_frame_size[1]),
            self.sprites
        )
        self.background_frame_rect = pg.Rect(self.to_scale(gs.career_background_frame_pos), self.to_scale(gs.career_background_frame_size))

        self.return_button_text = "<" # also hardcoded xd
        self.buttons["return"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_square"], "hover":self.sprites["button_template_square_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((gs.career_background_frame_pos[0] + gs.career_return_button_margin, gs.career_background_frame_pos[1] + gs.career_return_button_margin)), self.to_scale((gs.career_return_button_size, gs.career_return_button_size))),
            0,
            None,
            partial(self.scene_handler.setActiveScene, "main_menu"),
            None,
            self.app
        )

        self.selector_button_left_text = "<"
        self.selector_button_right_text = ">"

        self.career_selector_starting_position = (
            gs.career_background_frame_pos[0] + gs.career_selector_element_margin + self.buttons["return"].rect.right,
            gs.career_background_frame_pos[1] + gs.career_selector_element_margin
        )

        self.career_level_button_width = gs.career_level_window_size[0]
        self.career_level_button_height = 100
        self.career_level_button_offset = 10

        self.buttons["career_selector_left"] = button(
            flatpane("sprite", {"main":self.sprites["button_template_square"], "hover":self.sprites["button_template_square_dark"]}, sprite="main"),
            pg.Rect(self.to_scale((self.career_selector_starting_position[0], self.career_selector_starting_position[1])), self.to_scale((gs.career_return_button_size, gs.career_return_button_size))),
            0,
            None,
            partial(self.app.cycle_career, False),
            None,
            self.app
        )

        self.buttons["career_selector_right"] = button(
            flatpane("sprite", {"main":self.sprites["button_template_square"], "hover":self.sprites["button_template_square_dark"]}, sprite="main"),
            pg.Rect(self.to_scale((self.career_selector_starting_position[0] + gs.career_selector_display_width + gs.career_selector_element_height + 2 * gs.career_selector_element_margin, self.career_selector_starting_position[1])), self.to_scale((gs.career_return_button_size, gs.career_return_button_size))),
            0,
            None,
            partial(self.app.cycle_career, True),
            None,
            self.app
        )

        self.selector_display = UIFrameBuilder.get_ui_frame(
            self.to_scale_x(gs.career_selector_display_width),
            self.to_scale_y(gs.career_selector_element_height),
            self.sprites
        )

        self.selector_display_rect = pg.Rect(
            self.to_scale((self.career_selector_starting_position[0] + gs.career_selector_element_height + gs.career_selector_element_margin, self.career_selector_starting_position[1])),
            self.to_scale((gs.career_selector_display_width, gs.career_selector_element_height))
        )

        self.selector_display_text = self.texts["career_selector_no_career_loaded"] # you should never see this XD

        career_level_scrollbar = Scrollbar(
                                            appInstance         =self.app,
                                            pos                 =(gs.career_level_window_pos[0] + gs.career_level_window_size[0] + 20, gs.career_level_window_pos[1]),
                                            size                =(30, gs.career_level_window_size[1]),
                                            windowHeight        =gs.career_level_window_size[1],
                                            backgroundColor     =roket_dark_orange,
                                            floaterHeight       =60,
                                            floaterSprite       =self.sprite_handler.load_sprite("scrollbar_floater", "engine/game/assets/img/menu/scrollbar_floater.png", (30, 60), "c", False)
                                        )

        self.level_decoration_scroll_window = ScrollableWindow(
            appInstance             =self.app,
            pos                     =gs.career_level_decoration_window_pos,
            size                    =gs.career_level_decoration_window_size,
            scrollbar               =career_level_scrollbar,
            backgroundColor         =roket_light_blue,
            scrollSpeedMultiplier   =50
        )

        self.level_scroll_window = ScrollableWindow(
            appInstance             =self.app,
            pos                     =gs.career_level_window_pos,
            size                    =gs.career_level_window_size,
            scrollbar               =career_level_scrollbar,
            backgroundColor         =roket_light_blue,
            scrollSpeedMultiplier   =50
        )

        level_button_frame = UIFrameBuilder.get_ui_frame(
            self.career_level_button_width,
            self.career_level_button_height,
            self.sprites,
            background_sprite="ui_builder_background_light",
            alpha=True
        )

        self.sprites["level_button_frame"] = self.sprite_handler.real_scale_sprite(level_button_frame, level_button_frame.size)

        # create darker button variants
        for sprite in ["level_button_frame"]:
            dark_name = sprite+"_dark"
            self.sprites[dark_name] = self.sprites[sprite].copy()
            pg.Surface.fill(self.sprites[dark_name], BUTTON_COLOR_SUBTRACT_COLOR, special_flags=pg.BLEND_SUB)

        self.level_buttons = {}
        self.level_scroll_window.set_content(self.sprites["scaling_tester"]) # self.sprites["scaling_tester"]
        self.level_decoration_scroll_window.set_content(self.sprites["scaling_tester"]) # self.sprites["scaling_tester"]
        self.button_render_surface = None
        self.decoration_render_surface = None
