import json
from pathlib import Path

class JsonLoader:
    @staticmethod
    def create_new_file(filepath:str) -> None:
        try:
            Path(filepath.rsplit('/', 1)[0]).mkdir(parents=True, exist_ok=True)

            with open(filepath, "x") as file:
                return True
        except FileExistsError:
            return False

    @staticmethod
    def load_from_file(filepath:str) -> dict:
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except:
            print(f"JsonLoader:readError: couldn't read data from file {filepath}")
        
    @staticmethod
    def write_to_file(filepath:str, data:dict) -> None:
        """ try: """
        if JsonLoader.create_new_file(filepath):
            print(f"JsonLoader: created new file at {filepath}")
        with open(filepath, "w") as file:
            file.write(json.dumps(data, indent=4))
        """ except:
            print(f"JsonLoader:writeError: couldn't write data:\n{data}\nto file:\n{filepath}") """