from game.scripts.popup_windows.popup import PopupWindow

class PopupWindowYesNo(PopupWindow):
    def __init__(self, appInstance, content):
        self.app = appInstance
        super().__init__(appInstance, content, [self.app.texts["popup_window_choice_accept"], self.app.texts["popup_window_choice_refuse"]])