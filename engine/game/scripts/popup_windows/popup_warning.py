from game.scripts.popup_windows.popup import PopupWindow

class PopupWindowWarning(PopupWindow):
    def __init__(self, appInstance, content):
        self.app = appInstance
        super().__init__(appInstance, content, [self.app.texts["popup_window_warning_dismiss"]])