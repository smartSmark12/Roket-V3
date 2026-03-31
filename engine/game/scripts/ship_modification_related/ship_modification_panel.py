from game.scripts.pageable_panel.panel import Panel
from game.scripts.ship_modification_related.ship_modification_page import ShipModPage

class ShipModPanel(Panel):
    def __init__(self, pages:list[ShipModPage]=[]):
        super().__init__(pages)