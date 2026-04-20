from game.scripts.popup_windows.popup import PopupWindow

class PopupWindowInfo(PopupWindow):
    def __init__(self, appInstance, content):
        self.app = appInstance
        super().__init__(appInstance, content, self.app.texts["popup_window_info_dismiss"])