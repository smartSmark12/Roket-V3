class InteractiveVUI:
    def __init__(self, buttons: list):
        self.buttons = buttons

    def hover_detection(self):
        for button in self.buttons:
            button.activation_detection()