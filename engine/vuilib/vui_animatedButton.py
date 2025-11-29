from pygame import Rect
from engine.vuilib.vui_flatpane import flatpane
from vuilib.vui_button import button

class AnimatedButton(button):
    def __init__(self, flatpane_sprite: flatpane, rect: Rect | tuple, hold_time: int | float, on_hover_function, on_click_function, on_hold_function, appInstance):
        super().__init__(flatpane_sprite, rect, hold_time, on_hover_function, on_click_function, on_hold_function, appInstance)

    def do_animation(self, REPLACE_THIS_FUNCTION_WITH_ANIMATION): pass