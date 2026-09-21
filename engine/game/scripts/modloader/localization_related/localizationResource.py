class LocalizationResource:
    def __init__(self, code:str, name:str, paths:list[str]):
        self.code = code
        self.name = name
        self.paths = paths

    def add_path(self, path:str):
        if not path in self.paths:
            self.paths.append(path)
        else:
            print(f"{__name__}: path already registered")

    def get_code(self):
        return self.code
    
    def get_name(self):
        return self.name

    def get_paths(self):
        return self.paths