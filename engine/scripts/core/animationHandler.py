import os
import csv
import pygame as pg

from scripts.vanimlib.val_animatedTexture import AnimatedTexture
from scripts.renderItem import RenderItem
from vuilib.vui_flatpane_autoconvert import convert_to_flatpane
from scripts.core.settings import DEFAULT_ANIMATION_PATH, WIDTH, HEIGHT

class AnimationHandler:
    def __init__(self, appInstance):
        self.app = appInstance

    def initial_load(self):
        """ self.app.take_over_runtime_logger(f"{__name__}:animation_loader") """
        print(f"{__name__}: Starting initial animation compiling...\n")
        """ self.app.return_to_runtime_logger(f"{__name__}:animation_loader") """

        self.create_animations()

    def create_animations(self, filePath=DEFAULT_ANIMATION_PATH):

        self.app.take_over_runtime_logger(f"{__name__}:animation_loader")
        print(f"{__name__}: Beginning animation compiling...\n")

        with open(os.path.join(filePath), "r") as file:
            anim_reader = csv.reader(file)

            errors_assign = 0
            errors_position = 0
            errors_creation = 0

            for line in anim_reader:

                temp_frames = {}

                for item in range(len(line)):
                    if item not in [0, 1, 2, 3]:
                        try:
                            temp_frames[int(item)-4] = self.app.sprites[line[item]]
                        except:
                            errors_assign += 1
                            print(f"can't assign frame {item} of {line[0]}")

                try:
                    position = line[3].split(":")
                    position = (int(position[0]), int(position[1]))
                except:
                    errors_position += 1
                    print(f"couldn't read animation position of {line[0]}")

                """ try: """
                self.app.animations[line[0]] = AnimatedTexture(convert_to_flatpane(temp_frames), float(line[1]), int(line[2]), position, self.app) # need to remake this probably :>
                """ except:
                    errors_creation += 1
                    print(f"couldn't create animation {line[0]}") # need proper log """

        print(f"\n{__name__}:\n------------\nTotal loaded animations: {len(self.app.animations)}\nTotal animation loading errors: {errors_assign + errors_position + errors_creation} (a: {errors_assign}, p: {errors_position}, c: {errors_creation})\n")

        self.app.return_to_runtime_logger(f"{__name__}:animation_loader")

    def render_animations(self):
        for anim in self.app.animations:
            if anim in self.app.animations_to_render:
                anim_reference = self.app.animations[anim]

                anim_reference.update_active_frame(self.app.dt)
                position = self.app.animations[anim].get_animation_position()
                self.app.to_render.append(RenderItem("sprite", anim_reference.get_render_layer(), {"rect":(position[0], position[1], WIDTH, HEIGHT),"sprite":anim_reference.get_current_frame().sprite}))

