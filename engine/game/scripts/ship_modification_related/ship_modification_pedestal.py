from game.scripts.modloader.roket_body_related.roket_body       import RoketBody
from game.scripts.sprite_window                                 import SpriteWindow
from scripts.colors                                             import red
from scripts.core.settings                                      import MODULE_DEFAULT_SIZE

class ShipModInteractivePedestal:
    def __init__(self, appInstance, ship:RoketBody, position:tuple[float|int], size:tuple[float|int], slotEditingModeEnabled:bool=False):
        self.app = appInstance
        self.ship = ship
        self.pos = position
        self.size = size
        self.slot_editing_mode = slotEditingModeEnabled
        
        self.hovered_slot = None # a module panel slot; not the ship slot

        self.slot_offset = (
            self.app.to_scale_x(self.pos[0] + self.size[0] / 2) - self.app.sprites["pedestal_ship_slot"].get_width() / 2,
            self.app.to_scale_y(self.pos[1] + self.size[1] / 2) - self.app.sprites["pedestal_ship_slot"].get_height() / 2
        )

        self.line_slot_offset = (
            self.app.to_scale_x(self.pos[0] + self.size[0] / 2),
            self.app.to_scale_y(self.pos[1] + self.size[1] / 2)
        )
        
        self._regenerate_window()
        
    def _regenerate_window(self):
        self.window = SpriteWindow(
                    appInstance     =self.app,
                    sprite          =self.ship.get_sprites().get_active_sprite(), # oh how i hate flatpanes
                    pos             =self.pos,
                    size            =self.size,
                    renderLayer     =self.app.LAYER_UI_TOP_BOTTOM
                )
        
    def update(self):
        pass
    
    def set_module_slot_hovered(self, slot):
        self.hovered_slot = slot

    def _render_slots(self):
        for slot_id, slot in self.ship.get_module_slots().items():
            # draw slot background
            if self.slot_editing_mode and not slot.has_module():
                self.app.draw(
                    "sprite",
                    self.app.LAYER_UI_TOP_TOP,
                    {
                        "sprite":self.app.sprites["pedestal_ship_slot"],
                        "rect":((slot.get_pos()[0] / 2) * self.app.to_scale_x(self.size[0]) + self.slot_offset[0], (slot.get_pos()[1] / 2) * self.app.to_scale_y(self.size[1]) + self.slot_offset[1], 0, 0)
                    }
                )

            # draw slot module
            if slot.has_module():
                sprite = slot.get_module().get_sprites().get_active_sprite()
                sprite_size = MODULE_DEFAULT_SIZE[0] * slot.get_module().sizeModifier * self.window.ratio
                sprite = self.app.sprite_handler.cached_real_scale_sprite(sprite, (sprite_size, sprite_size))

                self.app.draw(
                    "sprite",
                    self.app.LAYER_UI_TOP_TOP,
                    {
                        "sprite":sprite, # omfg hello future debugging me
                        "rect":((slot.get_pos()[0] / 2) * self.app.to_scale_x(self.size[0]) + self.line_slot_offset[0] - sprite.get_width() / 2, (slot.get_pos()[1] / 2) * self.app.to_scale_y(self.size[1]) + self.line_slot_offset[1] - sprite.get_height() / 2, 0, 0)
                    }
                )

    
    def _render_connection_line(self):
        module = self.ship.get_module(self.hovered_slot.get_slot_id())

        line_start = self.app.to_scale(self.hovered_slot.get_ui_line_start())
        line_end = ((module.get_pos()[0] / 2) * self.app.to_scale_x(self.size[0]) + self.line_slot_offset[0], (module.get_pos()[1] / 2) * self.app.to_scale_y(self.size[1]) + self.line_slot_offset[1])
        
        self.app.draw("line", self.app.LAYER_UI_TOP_TOP_TOP, {"color":red, "start":line_start, "end":line_end, "width":6})
    
    def render(self):

        self._render_slots()
        
        if self.hovered_slot is not None and self.slot_editing_mode:
            self._render_connection_line()
        
        self.window.render()
    
    def set_ship(self, shipToSet:RoketBody):
        self.ship = shipToSet
        
        self._regenerate_window()