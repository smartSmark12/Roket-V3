class Navigator:
    def __init__(self, navigatorType):
        self.nav_type = navigatorType

    def move(self, appInstance):
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