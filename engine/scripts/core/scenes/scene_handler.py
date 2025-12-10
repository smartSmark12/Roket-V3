from scripts.core.scenes.scene import Scene
from scripts.core.settings import DEFAULT_SCENE_NAME

class SceneHandler:
    def __init__(self, appInstance):
        self.app = appInstance

        self.scenes = {}
        self.activeScene = DEFAULT_SCENE_NAME

    def addScene(self, sceneToAdd:Scene):
        if not sceneToAdd.name in self.scenes:
            self.scenes[sceneToAdd.name] = sceneToAdd
        else:
            print(f"{__name__}: Scene {sceneToAdd.name} already in scenes")

    def getScene(self, sceneName:str):
        if sceneName in self.scenes:
            return self.scenes[sceneName]
        else:
            print(f"{__name__}: Scene {sceneName} not found in scenes")
            return None

    def getActiveSceneName(self):
        return self.activeScene
    
    def getActiveScene(self):
        return self.scenes[self.activeScene]
    
    def setActiveScene(self, sceneName:str|None):
        if sceneName in self.scenes or sceneName == None:
            self.activeScene = sceneName
        else:
            print(f"{__name__}: Scene {sceneName} not found in scenes - no new active scene set")

    def updateScene(self):
        if self.getActiveSceneName() != None:
            self.getActiveScene().update()

    def renderScene(self):
        if self.getActiveSceneName() != None:
            self.getActiveScene().render()