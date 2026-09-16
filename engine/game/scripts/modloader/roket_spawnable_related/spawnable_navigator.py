from scripts.core.settings import HEIGHT

class Navigator:
    def __init__(self, appInstance, navigatorType):
        self.app = appInstance
        self.nav_type = navigatorType

        self.target_pos = None
        self.object = None # gets set immediately almost

    def set_object(self, object):
        self.object = object

    def set_target_pos(self, pos:tuple):
        self.target_pos = pos

    def get_start_pos(self):
        match self.nav_type:
            case "straight":
                return self.app.get_ingame_ship().get_pos()
            case "point":
                return self.app.get_ingame_ship().get_pos()
            case "s_point":
                if self.object.speed < 0: # moving up the screen
                    return (self.target_pos[0], HEIGHT + 200) # random number, change it pls
                else: # moving down the screen
                    return (self.target_pos[0], -200)
            case "asteroid":
                return self.app.get_ingame_ship().get_pos()
            case "spawnable":
                return self.app.get_ingame_ship().get_pos()

    def move(self): # move the object directly using self.object based on data from app
        match self.nav_type:
            case "straight":
                pass
            case "point":
                pass
            case "s_point":
                pass
            case "asteroid":
                pass
            case "spawnable":
                pass