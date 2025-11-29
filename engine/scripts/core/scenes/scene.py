from scripts.colors import magenta

class Scene:
    def __init__(self, appInstance, name):
        self.app = appInstance
        self.name = name

    def update(self):
        print(f"scene {self.name} updated! (override scene.update function)")

    def render(self):
        self.app.draw("text", self.app.LAYER_UI_TOP, {"text":f"{self.name} (override scene.render function)", "font":self.app.default_font, "color":magenta})