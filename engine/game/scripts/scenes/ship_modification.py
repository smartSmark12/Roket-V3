import pygame as pg

from game.scripts.scenes.intermediate_scene                             import IntermediateScene
from game.scripts.scenes.global_scene_params                            import GlobalSceneParams as gs

from scripts.core.settings                                              import GAME_VERSION, GAME_VERSION_HINT, WIDTH, HEIGHT, SLOTS_IN_SHIP_MOD_PAGE, SLOTS_IN_SHIP_MOD_STORAGE_PAGE
from vuilib.vui_flatpane                                                import flatpane
from vuilib.vui_button                                                  import button
from game.scripts.vuilib_extension.text_button                          import TextButton
from functools                                                          import partial
from game.scripts.ui_frame_builder                                      import UIFrameBuilder
from game.scripts.sprite_window                                         import SpriteWindow
from game.scripts.ship_modification_related.ship_modification_panel     import ShipModPanel
from game.scripts.ship_modification_related.ship_modification_pedestal  import ShipModInteractivePedestal

class ShipModificationScene(IntermediateScene):
    def __init__(self, appInstance):
        super().__init__(appInstance, "ship_modification")

        self.buttons = {}

        self.background_frame = UIFrameBuilder.get_ui_frame(
            self.to_scale_x(gs.ship_mod_background_frame_size[0]),
            self.to_scale_y(gs.ship_mod_background_frame_size[1]),
            self.sprites
        )
        self.background_frame_rect = pg.Rect(self.to_scale(gs.ship_mod_background_frame_pos), self.to_scale(gs.ship_mod_background_frame_size))

        ### hangar text
        self.hangar_text = "// " + self.texts["ship_hangar_hangar_text"]
        self.hangar_text_rect = pg.Rect( # DONT use this rect as a reference - to_scale applied
            self.to_scale_x(gs.ship_mod_background_frame_pos[0] + gs.ship_mod_return_button_size + gs.ship_mod_return_button_margin + 20),
            self.to_scale_y(gs.ship_mod_background_frame_pos[1] + 50),
            0,
            0
        )

        ### available mod slot window
        self.ship_slot_size = (400, 100)
        self.ship_slot_margin = 20

        #ship_mod_slot_button_size = 100
        
        ### ship mod pedestal
        self.pedestal_pos = (730, 400) # this is kinda stupid, no?
        self.pedestal_size = (400, 400)

        # eh idk just resize the fking button
        self.sprites["button_template_square_smaller"] = self.sprite_handler.real_scale_sprite(self.sprites["button_template_square"], (gs.ship_mod_slot_button_size, gs.ship_mod_slot_button_size))
        self.sprites["button_template_square_smaller_dark"] = self.sprite_handler.real_scale_sprite(self.sprites["button_template_square_dark"], (gs.ship_mod_slot_button_size, gs.ship_mod_slot_button_size))

        self.ship_mod_panel_size = (
            self.ship_slot_size[0] + 2 * self.ship_slot_margin,
            (SLOTS_IN_SHIP_MOD_PAGE + 1) * (self.ship_slot_size[1] + self.ship_slot_margin) + self.ship_slot_margin # the +1 is for the page buttons under
        )
        self.ship_mod_panel_pos = (
            gs.ship_mod_background_frame_pos[0] + self.ship_slot_margin,
            gs.ship_mod_background_frame_pos[1] + 200
        )

        self.slot_panel = ShipModPanel() # regenerated later in main engine

        self.slot_panel_background = UIFrameBuilder.get_ui_frame(
            self.to_scale_x(self.ship_mod_panel_size[0]),
            self.to_scale_y(self.ship_mod_panel_size[1]),
            self.sprites,
            alpha=True
        )

        self.slot_panel_rect = pg.Rect(self.to_scale(self.ship_mod_panel_pos), self.to_scale(self.ship_mod_panel_size))

        self.buttons["slot_page_left"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_square_smaller"], "hover":self.sprites["button_template_square_smaller_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((self.ship_mod_panel_pos[0] + self.ship_slot_margin, self.ship_mod_panel_pos[1] + SLOTS_IN_SHIP_MOD_PAGE * (self.ship_slot_size[1] + self.ship_slot_margin) + self.ship_slot_margin)), self.to_scale((gs.ship_mod_slot_button_size, gs.ship_mod_slot_button_size))),
            0,
            None,
            partial(self.slot_panel.prev_page),
            None,
            self.app
        )

        self.buttons["slot_page_right"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_square_smaller"], "hover":self.sprites["button_template_square_smaller_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((self.ship_mod_panel_pos[0] + self.ship_slot_size[0] - gs.ship_mod_slot_button_size + self.ship_slot_margin, self.ship_mod_panel_pos[1] + SLOTS_IN_SHIP_MOD_PAGE * (self.ship_slot_size[1] + self.ship_slot_margin) + self.ship_slot_margin)), self.to_scale((gs.ship_mod_slot_button_size, gs.ship_mod_slot_button_size))),
            0,
            None,
            partial(self.slot_panel.next_page),
            None,
            self.app
        )

        self.page_button_left_text = "<" # do you realistically need a translation for this?? The answer is no, shut up.
        self.page_button_right_text = ">"

        ### ship window
        ### module storage window
        self.storage_slot_size = (100, 100)
        self.storage_slot_margin = 20

        self.storage_panel_size = (
            (self.storage_slot_size[0] + self.storage_slot_margin) * SLOTS_IN_SHIP_MOD_STORAGE_PAGE[0] + self.storage_slot_margin,
            (SLOTS_IN_SHIP_MOD_STORAGE_PAGE[1] + 1) * (self.storage_slot_size[1] + self.storage_slot_margin) + self.storage_slot_margin # the +1 is for the page buttons under
        )

        self.storage_panel_pos = (
            gs.ship_mod_background_frame_pos[0] + gs.ship_mod_background_frame_size[0] - (self.storage_panel_size[0] + self.ship_slot_margin),
            gs.ship_mod_background_frame_pos[1] + self.ship_slot_margin
        )

        self.storage_panel = ShipModPanel()
        #self.regenerate_ship_mod_slot_panel()

        self.storage_panel_background = UIFrameBuilder.get_ui_frame(
            self.to_scale_x(self.storage_panel_size[0]),
            self.to_scale_y(self.storage_panel_size[1]),
            self.sprites,
            alpha=True
        )

        self.storage_panel_rect = pg.Rect(self.to_scale(self.storage_panel_pos), self.to_scale(self.storage_panel_size))

        self.active_ship_module = None

        ### ship mod buttons
        self.return_button_text = "<" # yes, this is hardcoded. judge me.

        self.buttons["return"] = button(
            flatpane(
                "sprite",
                {"main":self.sprites["button_template_square"], "hover":self.sprites["button_template_square_dark"]},
                sprite="main"
            ),
            pg.Rect(self.to_scale((gs.ship_mod_background_frame_pos[0] + gs.ship_mod_return_button_margin, gs.ship_mod_background_frame_pos[1] + gs.ship_mod_return_button_margin)), self.to_scale((gs.ship_mod_return_button_size, gs.ship_mod_return_button_size))),
            0,
            None,
            partial(self.scene_handler.setActiveScene, "main_menu"),
            None,
            self.app
        )

        ### ship mod pedestal
        self.pedestal = ShipModInteractivePedestal(
            self.app,
            self.app.get_active_ship(),
            self.pedestal_pos,
            self.pedestal_size
        )