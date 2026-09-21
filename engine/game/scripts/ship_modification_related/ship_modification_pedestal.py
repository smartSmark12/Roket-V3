from game.scripts.modloader.roket_body_related.roket_body       import RoketBody
from game.scripts.sprite_window                                 import SpriteWindow
from scripts.colors                                             import red

class ShipModInteractivePedestal:
    def __init__(self, appInstance, ship:RoketBody, position:tuple[float|int], size:tuple[float|int]):
        self.app = appInstance
        self.ship = ship
        self.pos = position
        self.size = size
        
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
        for slot_id, slot in self.ship.get_modules().items():
            self.app.draw(
                "sprite",
                self.app.LAYER_UI_TOP_TOP,
                {
                    "sprite":self.app.sprites["pedestal_ship_slot"],
                    "rect":((slot.get_pos()[0] / 2) * self.app.to_scale_x(self.size[0]) + self.slot_offset[0], (slot.get_pos()[1] / 2) * self.app.to_scale_y(self.size[1]) + self.slot_offset[1], 0, 0)
                }
            )

            #print(slot_id, (slot.pos[0] * self.app.to_scale_x(self.size[0]) + self.slot_offset[0], slot.pos[1] * self.app.to_scale_y(self.size[1]) + self.slot_offset[1]))
    
    def _render_connection_line(self):
        module = self.ship.get_module(self.hovered_slot.get_slot_id())

        line_start = self.app.to_scale(self.hovered_slot.get_ui_line_start())
        line_end = ((module.get_pos()[0] / 2) * self.app.to_scale_x(self.size[0]) + self.line_slot_offset[0], (module.get_pos()[1] / 2) * self.app.to_scale_y(self.size[1]) + self.line_slot_offset[1])
        
        self.app.draw("line", self.app.LAYER_UI_TOP_TOP_TOP, {"color":red, "start":line_start, "end":line_end, "width":6})
    
    def render(self):

        self._render_slots()
        
        if self.hovered_slot is not None:
            self._render_connection_line()
        
        self.window.render()
    
    def set_ship(self, shipToSet:RoketBody):
        self.ship = shipToSet
        
        self._regenerate_window()