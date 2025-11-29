import pygame as pg
import os
import csv

from scripts.core.settings import DEFAULT_SPRITE_PATH, DEFAULT_SPRITE_JSON_PATH, WIDTH, HEIGHT
from scripts.json_loader import JsonLoader

class SpriteHandlerJSON:
    def __init__(self, appInstance):
        self.app = appInstance
        
    def initial_load(self):
        print(f"{__name__}: Starting initial sprite loading (using SpriteHandlerJSON)...\n")
        self.load_sprites()

    def load_sprites(self, filePath=DEFAULT_SPRITE_JSON_PATH):
        self.app.take_over_runtime_logger(f"{__name__}:sprite_loader_json")
        print(f"{__name__}: Beginning JSON sprite loading...\n")

        errors = {
            "r":0,
            "m":0,
            "s":0,
            "c":0
        }

        try:
            json_data = JsonLoader.load_from_file(filePath)
        except:
            errors["r"] += 1
            

        for file_name in json_data:
            file = json_data[file_name]

            try:
                image = pg.image.load(os.path.join(file[0]))
            except:
                print(f"can't load {file_name} into memory")
                errors["m"] += 1

            if file[1] != None:
                try:
                    """ image = pg.transform.scale(image, (file[1][0], file[1][1])) """
                    image = self.real_scale_sprite(image, (file[1][0], file[1][1]))
                except:
                    print(f"can't scale {file_name} to size {float(file[1][0])}:{float(file[1][1])}")
                    errors["s"] += 1

            try:
                match file[2]:
                    case "c": image = image.convert()
                    case "ca": image = image.convert_alpha()
                    case _: pass # no convert
            except:
                print(f"can't convert {file_name}")
                errors["c"] += 1

            self.app.sprites[file_name] = image

        print(f"\n{__name__}:\n------------\nTotal loaded sprites: {len(self.app.sprites)}\nTotal sprite loading errors: {errors["r"] + errors['m'] + errors['s'] + errors['c']} (r: {errors['r']}, m: {errors['r']}, s: {errors["s"]}, c: {errors['c']})\n")

        self.app.return_to_runtime_logger(f"{__name__}:sprite_loader_json")

    def rescale_sprites(self, spritesToRescale:dict): ## currently unfinished
        rescaled_sprites = {}

        for sprite in spritesToRescale:
            rescaled_sprites[sprite] = self.rescale_sprite()

        return rescaled_sprites

    def rescale_sprite(self, spriteToRescale:pg.Surface, size:tuple|list) -> pg.Surface:
        return pg.transform.scale(spriteToRescale, (size[0], size[1]))
    
    def real_scale_sprite(self, spriteToRescale:pg.Surface, size:tuple|list) -> pg.Surface:
        return self.rescale_sprite(spriteToRescale, (self.to_scalex(size[0]), self.to_scaley(size[1])))
    
    def real_scale_sprites(self, spritesToRescale:dict[str, pg.Surface], sizes:dict[str, [int, int]]):
        rescaled_sprites = {}

        for i in spritesToRescale:
            sprite = spritesToRescale[i]

            rescaled_sprites[i] = self.real_scale_sprite(sprite, sizes[i])

        return rescaled_sprites

    def get_scale(self):
        self.app.screen_scale = (WIDTH/1920, HEIGHT/1080)

    def to_scalex(self, number: float | int, round_num: bool = True):
        if round_num: return round(number * self.app.screen_scale[0])
        else: return number * self.app.screen_scale[0]
    
    def to_scaley(self, number: float | int, round_num: bool = True):
        if round_num: return round(number * self.app.screen_scale[1])
        else: return number * self.app.screen_scale[1]

# the old version
class SpriteHandler:
    def __init__(self, appInstance):
        self.app = appInstance

    def initial_load(self):
        """ self.app.take_over_runtime_logger(f"{__name__}:sprite_loader") # just some main engine stuff :| """
        print(f"{__name__}: Starting initial sprite loading (using SpriteHandler)...\n")
        """ self.app.return_to_runtime_logger(f"{__name__}:sprite_loader") """

        self.load_sprites()

    def load_sprites(self, filePath=DEFAULT_SPRITE_PATH):
        self.app.take_over_runtime_logger(f"{__name__}:sprite_loader")
        print(f"{__name__}: Beginning sprite loading...\n")

        errors_read = 0
        errors_memory = 0
        errors_scale = 0
        errors_convert = 0

        with open(os.path.join(filePath), "r") as file:
            self.reader = csv.reader(file)

            for line in self.reader:
                try:
                    print(f"read {line[0]}:{line[1]}:{line[2]}:{line[3]}")
                except:
                    print(f"can't read {line} from file")
                    errors_read += 1

                try:
                    self.app.sprites[line[1]] = pg.image.load(os.path.join(line[0]))
                except:
                    print(f"can't load {line[1]} into memory")
                    errors_memory += 1

                if line[2] != "None":
                    try:
                        scale = line[2].split(":")
                        self.app.sprites[line[1]] = pg.transform.scale(self.app.sprites[line[1]], (float(scale[0]), float(scale[1])))
                    except:
                        print(f"can't scale {line[1]} to size {float(scale[0])}:{float(scale[1])}")
                        errors_scale += 1
                
                if line[3] == "c":
                    try:
                        self.app.sprites[line[1]] = self.app.sprites[line[1]].convert()
                    except:
                        print(f"can't convert {line[1]}")
                        errors_convert += 1

                elif line[3] == "ca":
                    try:
                        self.app.sprites[line[1]] = self.app.sprites[line[1]].convert_alpha()
                    except:
                        print(f"can't convert {line[1]}")
                        errors_convert += 1


            print(f"\n{__name__}:\n------------\nTotal loaded sprites: {len(self.app.sprites)}\nTotal sprite loading errors: {errors_read + errors_memory + errors_scale + errors_convert} (r: {errors_read}, m: {errors_memory}, s: {errors_scale}, c: {errors_scale})\n")

            for i in self.app.sprites:
                print(f"{i}\n{self.app.sprites[i]}\n")

        self.app.return_to_runtime_logger(f"{__name__}:sprite_loader")
