# Nebula Game Framework prototype v0.0.4s (29. 11. 2025) [so much shis istg + s for scenes]
# NGFp designed by VaclavK - not for commercial use - only experiments and silly stuff >:)

## DO NOT USE mainEngine.py AS AN ENTRY POINT
## LOCATE THE EXECUTABLE IN THE TOP PARENT DIRECTORY

import pygame as pg # pygame; the game library this GF is built on
import random # used for generating random numbers
import sys # used for handling script access
sys.path.append('../engine')
import csv # used for saving and loading data into and from .csv files
import os # used for handling file access and system calls
import math # math
import moderngl as mgl
from array import array
from threading import Lock
import _thread
from scripts.core.render import MainGameRender, ThreadedGameRenderer # local renderer library
from scripts.renderItem import RenderItem # local class library serving as the base for every object rendering to the screen
from scripts.functions import * # local universal functions library
from scripts.core.settings import * # local system settings
from scripts.colors import * # local library containing basic colors
from vuilib.vuilib import * # local ui QoL library
from vuilib.vui_flatpane import flatpane
from vuilib.vui_flatpane_autoconvert import convert_to_flatpane
from vuilib.vui_button import button
from vuilib.vui_interactive import InteractiveVUI
from scripts.vanimlib.val_animatedTexture import AnimatedTexture # local library for easier work with image sequences and video frames
from scripts.runtimeLogHandler import LogHandler # local library for terminal and log handling
from scripts.core.fileManager import FileManager
from scripts.mplib.multiplayerClient import mpClient # client+network from multiplayerlib for multiplayer data handling
from scripts.tileScripts.VTileGen import VTileGenerator # useful for generating custom size maps with set content using VR (Vaclav-Random XD) distribution
from scripts.tileScripts.VTIleTerrainGen import VTileTerrainGenerator # used to generate terrain based on weights
from scripts.core.spriteHandler import SpriteHandler, SpriteHandlerJSON # local library used to handle sprite importing and rescaling
from scripts.core.animationHandler import AnimationHandler # local library used to create animations from imported sprites
from scripts.core.keyHandler import KeyHandler # local library used to handle key input changes
from scripts.core.openglHandler import OGLHandler # local library for shader support (experimental!)
from scripts.core.scenes.scene_handler import SceneHandler
from scripts.core.scenes.scene import Scene
from scripts.json_loader import JsonLoader
from scripts.core.settings import GAME_NAME, DEFAULT_SCENE_NAME
""" from game.game import MainGame """

## example import
from scripts.tileScripts.baseBiomeWeights import baseBiomeWeights

from functools import partial

# something like from engine.scripts import * using https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi46Of9hr-GAxVQhf0HHXmICu4QFnoECCYQAQ&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F1057431%2Fhow-to-load-all-modules-in-a-folder&usg=AOvVaw3vlcgC_pzadT7glu9LmH2n&cshid=1717404751563860&opi=89978449
# need to make a crash handler (official python function??)

class MainEngine:
    # pls do not touch, write your code in 'game_on_init'
    def __init__(self):
        pg.init()

        self.engine_on_init()
        self.game_on_init()

    # pls do not touch, contains only framework functions
    def engine_on_init(self):
        # default pygame-based variables
        self.is_running = True
        self.name = f"{GAME_NAME} (ngf_v:{NGF_VERSION})"
        self.clock = pg.time.Clock()
        self.dt = 0

        # load default font
        self.default_font = pg.font.SysFont("Arial", 50)

        # debug if opengl crashes
        print("OpenGL/ModernGL: ", OGL_ENABLED)

        # creates pygame window

        ### modified engine code go brrr
        # debug shis
        self.DEBUG_RESOLUTION_INDEX = 1

        self.create_resolutions()
        self.set_resolution()
        self.create_draw_window()

        ## need to redo this part
        if IN_FULLSCREEN:
            if OGL_ENABLED:
                self.render_window = pg.display.set_mode(self.active_resolution, pg.FULLSCREEN | pg.OPENGL | pg.DOUBLEBUF)
                self.window = pg.Surface(self.active_resolution)
            else:
                self.window = pg.display.set_mode(self.active_resolution, pg.FULLSCREEN)
        else:
            if OGL_ENABLED:
                self.render_window = pg.display.set_mode(self.active_resolution, pg.OPENGL | pg.DOUBLEBUF)
                self.window = pg.Surface(self.active_resolution)
            else:
                self.window = pg.display.set_mode(self.active_resolution)

        # opengl setup
        self.ogl_handler = OGLHandler(self)
        if OGL_ENABLED:
            self.ogl_handler.OGL_init()

        # rendering setup
        self.render_layers = RENDER_LAYERS # change in setting file (engine -> scripts -> core -> settings.py)

        self.LAYER_UI_TOP = 9

        self.animations_to_render = []
        self.to_render = []
        self.to_render_full = [] # for use in multithreaded rendering; no touchy >:3
        self.sprites = {}
        self.animations = {}

        self.sprite_handler = SpriteHandlerJSON(self) #SpriteHandler(self)
        # override default sprite_handler scale setup mode
        self.sprite_handler.get_scale(self.width, self.height) # gets the real screen scale for different resolutions (use self.sprite_handler.real_scale_sprite())
        self.sprite_handler.initial_load()

        self.animation_handler = AnimationHandler(self)
        self.animation_handler.initial_load() # must be after the sprite_handler init

        self.thread_lock = Lock() # shared lock for multithreading

        if MULTITHREADED_RENDERING:
            self.renderer = ThreadedGameRenderer(self, self.thread_lock)
        else:
            self.renderer = MainGameRender(self)

        # key handler setup
        self.keyhandler = KeyHandler(self) # change keybinds in keyhandler.py
        self.keyhandler.initial_setup()

        # scene handler setup
        self.scene_handler = SceneHandler(self)

        """ self.create_examples() """

        self.to_scale_x = self.sprite_handler.to_scalex
        self.to_scale_y = self.sprite_handler.to_scaley

        # logger setup
        self.create_runtime_logger()

        ## mouse last pressed status?? Why here?
        self.mouse_last = 0

    # write your game on_init here
    def game_on_init(self):
        # set render layers
        self.LAYER_UI_BOTTOM = 7

        # assign empty corrected mouse info
        self.corrected_mouse_info = None

        # load fonts # can hardcode, cause you'll still need to relaunch the game to take effect
        self.h1_font = pg.Font(DEFAULT_FONT_PATH, int(H1_FONT_SIZE * (self.height / HEIGHT)))
        self.button_font = pg.Font(DEFAULT_FONT_PATH, int(BUTTON_FONT_SIZE * (self.height / HEIGHT)))
        self.version_font = pg.Font(DEFAULT_FONT_PATH, int(VERSION_FONT_SIZE * (self.height / HEIGHT)))

        # load localization
        self.localization_code = DEFAULT_LOCALIZATION_CODE ## temp
        self.load_localization()

        # load keybinds
        self.keybind_path = DEFAULT_KEYBIND_PATH ## also temp
        self.load_keybinds()

        # create darker button variants
        BUTTON_COLOR_SUBTRACT_COLOR = (30, 30, 30)
        for sprite in ["button_template", "mainmenu_settings_button", "mainmenu_leaderboard_button"]:
            dark_name = sprite+"_dark"
            self.sprites[dark_name] = self.sprites[sprite].copy()
            pg.Surface.fill(self.sprites[dark_name], BUTTON_COLOR_SUBTRACT_COLOR, special_flags=pg.BLEND_SUB)

        # add all scenes
        self.scene_handler.addScene(Scene(self, "title"))
        self.scene_handler.addScene(Scene(self, "main_menu"))
        self.scene_handler.addScene(Scene(self, "ship_modification"))
        self.scene_handler.addScene(Scene(self, "game"))
        self.scene_handler.addScene(Scene(self, "career"))
        self.scene_handler.addScene(Scene(self, "achievements"))
        self.scene_handler.addScene(Scene(self, "settings"))

        # set main scene
        self.scene_handler.setActiveScene("title")

        title_scene = self.scene_handler.getScene("title")
        main_menu_scene = self.scene_handler.getScene("main_menu")
        ship_mod_scene = self.scene_handler.getScene("ship_modification")
        game_scene = self.scene_handler.getScene("game")
        career_scene = self.scene_handler.getScene("career")
        achievements_scene = self.scene_handler.getScene("achievements")
        settings_scene = self.scene_handler.getScene("settings")

        # override scene updates
        title_scene.update = self.title_update
        main_menu_scene.update = self.main_menu_update

        # override scene renders
        title_scene.render = self.title_render
        main_menu_scene.render = self.main_menu_render

        # override scene shis

        title_button_width = 280
        title_button_height = 128

        title_square_button_size = 128
        title_side_button_x_distance = 250
        title_button_y_offset = 160 # not sure why this cant be the same as button x dist ::

        main_menu_button_start_y = 650 # all values autoconverted by to_scale_x/y
        main_menu_button_width = title_button_width
        main_menu_button_height = title_button_height
        main_menu_button_y_offset = title_button_y_offset

        ## title

        title_scene.main_text = self.texts["title_title"]
        title_scene.version_text = "v" + GAME_VERSION + " - " + GAME_VERSION_HINT
        title_scene.play_text = self.texts["title_play"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_forward")
        title_scene.exit_text = self.texts["title_exit"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_back")
        title_scene.buttons = {}

        ## main_menu
        main_menu_scene.launch_text = self.texts["main_menu_launch"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_forward")
        main_menu_scene.return_text = self.texts["main_menu_return"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_back")
        main_menu_scene.buttons = {}


        ## create all title buttons
        title_scene.buttons["play"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_button_width) / 2), self.to_scale_y((HEIGHT - title_button_height) / 2), self.to_scale_x(title_button_width), self.to_scale_y(title_button_height)), 0, None, partial(self.scene_handler.setActiveScene, "main_menu"), None, self)
        title_scene.buttons["exit"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_button_width) / 2), self.to_scale_y((HEIGHT - title_button_height) / 2 + title_button_y_offset), self.to_scale_x(title_button_width), self.to_scale_y(title_button_height)), 0, None, partial(self.exit_game), None, self)
        
        title_scene.buttons["settings"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_settings_button"], "hover":self.sprites["mainmenu_settings_button_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_square_button_size) / 2 - title_side_button_x_distance), self.to_scale_y((HEIGHT - title_square_button_size) / 2), self.to_scale_x(title_square_button_size), self.to_scale_y(title_square_button_size)), 0, None, partial(print, "options pressed"), None, self)
        title_scene.buttons["achievements"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_leaderboard_button"], "hover":self.sprites["mainmenu_leaderboard_button_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_square_button_size) / 2 + title_side_button_x_distance), self.to_scale_y((HEIGHT - title_square_button_size) / 2), self.to_scale_x(title_square_button_size), self.to_scale_y(title_square_button_size)), 0, None, partial(print, "achievements pressed"), None, self)

        ## create all main_menu buttons
        main_menu_scene.buttons["launch"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - main_menu_button_width) / 2), self.to_scale_y(main_menu_button_start_y), self.to_scale_x(main_menu_button_width), self.to_scale_y(main_menu_button_height)), 0, None, partial(print, "launch pressed"), None, self)
        main_menu_scene.buttons["return"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - main_menu_button_width) / 2), self.to_scale_y(main_menu_button_start_y + main_menu_button_y_offset), self.to_scale_x(main_menu_button_width), self.to_scale_y(main_menu_button_height)), 0, None, partial(self.scene_handler.setActiveScene, "title"), None, self)


    def create_resolutions(self):
        # set possible resolutions
        self.RESOLUTIONS = [
            (1920, 1080),
            (1280, 720),
            (640, 360),
            (2560, 1440),
            (1280, 960),
            (1440, 1080),
            (80,45),
            (1200, 400)
        ]

    def set_resolution(self):
        self.active_resolution_index =  self.DEBUG_RESOLUTION_INDEX#4
        self.active_resolution = self.RESOLUTIONS[self.active_resolution_index]

        self.window_width = self.active_resolution[0] # fawak this is shis
        self.window_height = self.active_resolution[1]

    def create_draw_window(self):
        # extend the screen if ratio not 16:9
        target_ratio = 16/9
        current_ratio = self.window_width/self.window_height
        
        if current_ratio < target_ratio: # higher - wider, lower - taller
            self.width = self.window_width
            self.height = int(self.window_width / target_ratio)

        elif current_ratio > target_ratio:
            self.height = self.window_height
            self.width = int(self.window_height * target_ratio)

        else:
            self.width, self.height = self.window_width, self.window_height

        # create the actual draw window
        self.draw_window = pg.Surface((self.width, self.height))

        # assign blackbar sizes
        self.blackbar_x_size_aka_renderer_blit_x_offset = int((self.window_width - self.width) / 2)
        self.blackbar_y_size_aka_renderer_blit_y_offset = int((self.window_height - self.height) / 2)

    def load_localization(self):
        self.texts = {}

        # load default localization
        loaded_localization = JsonLoader.load_from_file(LOCALIZATION_PATH + DEFAULT_LOCALIZATION_CODE + LOCALIZATION_POSTFIX)

        self.texts = loaded_localization["texts"]

        # load new localization
        loaded_localization = JsonLoader.load_from_file(LOCALIZATION_PATH + self.localization_code + LOCALIZATION_POSTFIX)

        # replace default localization
        for text in loaded_localization["texts"]:
            self.texts[text] = loaded_localization["texts"][text]

    def load_keybinds(self):
        loaded_keybinds = JsonLoader.load_from_file(DEFAULT_KEYBIND_PATH)

        self.keyhandler.keybinds = loaded_keybinds

        self.keyhandler.update_keybind_buffers()

        print(loaded_keybinds)

    def register_keybind(self, keybind_name:str, keycode:int):
        self.keyhandler.register_keybind(keybind_name, keycode)
        pass # add keybind to the keyhandler

    def unregister_keybind(self, keybind_name:str, keycode:int):
        self.keyhandler.unregister_keybind(keybind_name, keycode)
        pass # remove keybind from the kh

    def save_keybinds(self):

        keybind_data = self.keyhandler.keybinds

        JsonLoader.write_to_file(ACTIVE_KEYBIND_PATH, keybind_data)
        print(f"{__name__}: saved keybinds to {ACTIVE_KEYBIND_PATH}")
        pass # save kbs to the json file

    def reset_keybinds(self):
        loaded_keybinds = JsonLoader.load_from_file(DEFAULT_KEYBIND_PATH)

        self.keyhandler.keybinds = loaded_keybinds

        self.keyhandler.update_keybind_buffers()

        self.save_keybinds()
        

    def title_update(self):
        title = self.scene_handler.getScene("title")
        # update all buttons
        for button_index in title.buttons:
            button = title.buttons[button_index]
            button.activation_detection(self.corrected_mouse_info)
            button.update_hold_time(self.corrected_mouse_info)

        # check for keybind activation
        if self.get_keybind_just_pressed("ui_forward"):
            title.buttons["play"].on_click()

        if self.get_keybind_just_pressed("ui_back"):
            title.buttons["exit"].on_click()

        ## unrelated temp debug until UI works
        if self.get_keybind_just_pressed("debug_reset_keybinds"):
            self.reset_keybinds()

    def title_render(self):
        title = self.scene_handler.getScene("title")

        # draw title
        self.draw("text", self.LAYER_UI_TOP, {"text":title.main_text, "no_bg":True, "font":self.h1_font, "center":(self.width/2, self.height/5)})

        # draw version info
        self.draw("text", self.LAYER_UI_TOP, {"text":title.version_text, "no_bg":True, "font":self.version_font, "rect":pg.Rect(self.to_scale_x(30), self.to_scale_y(HEIGHT - 50), 0, 0), "color":gray})

        # draw button texts
        self.draw_button_text(title.play_text, title.buttons["play"])
        self.draw_button_text(title.exit_text, title.buttons["exit"])

        for button in title.buttons:
            title.buttons[button].render()

    def main_menu_update(self):
        main_menu = self.scene_handler.getScene("main_menu")
        # update all buttons
        for button_index in main_menu.buttons:
            button = main_menu.buttons[button_index]
            button.activation_detection(self.corrected_mouse_info)
            button.update_hold_time(self.corrected_mouse_info)

        # check for keybind activation
        if self.get_keybind_just_pressed("ui_forward"):
            main_menu.buttons["launch"].on_click()

        if self.get_keybind_just_pressed("ui_back"):
            main_menu.buttons["return"].on_click()

    def main_menu_render(self):
        main_menu = self.scene_handler.getScene("main_menu")
        
        # draw button texts
        self.draw_button_text(main_menu.launch_text, main_menu.buttons["launch"])
        self.draw_button_text(main_menu.return_text, main_menu.buttons["return"])

        for button in main_menu.buttons:
            main_menu.buttons[button].render()

    def draw_button_text(self, buttonText:str, button):
        self.draw("text", self.LAYER_UI_TOP, {"text":buttonText, "no_bg":True, "font":self.button_font, "center":button.rect.center, "color":black})

    def screen_to_game_coords(self, pos) -> tuple:
        return (pos[0] - self.blackbar_x_size_aka_renderer_blit_x_offset, pos[1] - self.blackbar_y_size_aka_renderer_blit_y_offset)
    
    def get_keybind_pressed(self, keybind:str):
        return self.keybinds_pressed[keybind]
    
    def get_keybind_changed(self, keybind:str):
        return self.keybinds_changed[keybind]
    
    def get_keybind_just_pressed(self, keybind:str):
        return self.get_keybind_pressed(keybind) and self.get_keybind_changed(keybind)

    def get_keybind_keycode_name(self, keybind:str):
        return self.keyhandler.keybind_keycode_names[keybind]
    
    def get_keybind_keycode_name_in_square_brackets(self, keybind): # returns a shortened and capitalized version
        start = 0
        length = 3
        return "[" + self.get_keybind_keycode_name(keybind)[start : start + length].upper() + "]"

    def exit_game(self):
        print(f"{__name__}: exiting game")
        self.is_running = False

    def create_runtime_logger(self):
        self.logger = LogHandler()

    def ext_append_to_log(self, message):
        self.logger.add_to_log(message)

    def collect_logs(self):
        for module in [self.renderer.render_get_log()]:
            for item in module:
                self.ext_append_to_log(item)

    def print_log(self):
        self.logger.print_log()

    def take_over_runtime_logger(self, place):
        print(f"{place}: Taking over runtime log handler")

    def return_to_runtime_logger(self, place):
        print(f"{place}: Returning to runtime log handler")

    def create_examples(self):

        # vui example
        """ example_imgs = []
        example_imgs.append((flatpane("img", self.sprites, sprite="space_back").sprite, (0, 0)))
        for i in range(3):
            for j in range(4):
                example_imgs.append((flatpane("img", self.sprites, sprite="space_button").sprite, (200*j+10, 110*i+10))) """

        """ self.vui_example = VUILib.create_static_vui((RESOLUTION[0]//2, RESOLUTION[1]//2), False, (4*200+10, 3*110+10), example_imgs, True, 5) """

        """ # animation example
        example_anim = AnimatedTexture(convert_to_flatpane({"anim0":self.sprites["anim0"], "anim1":self.sprites["anim1"], "anim2":self.sprites["anim2"]}), 1) """

    	# vtilemap examples
        """ self.color_examples = [lime, green, gray, yellow, blue] """

            # vtile diamond map
        """ self.vtilemap_example = VTileGenerator.generateMap((38*4, 22*4), [0, 1, 2, 3, 4], "square", 20) """ # 38, 22; vk, square

            # vtile randomdist map
        """ mapsize = (38*6, 22*6)
        self.vtilemap_example = VTileGenerator.createEmptyMap(mapsize)
        self.vtilemap_example = VTileGenerator.placeStartingPoints(self.vtilemap_example, [0, 1, 2, 3, 4], 40)
        self.vtile_timer = 0 """

            # vtile terrain map full
        """ self.vtilemap_example = VTileTerrainGenerator.generateTerrainMap((38*5, 22*5), None, 4.5, 1) # stability = 2 """

            # vtile terrain map generable
        """ self.mapSize = (38*6, 22*6)
        self.vtilemap_example = VTileTerrainGenerator.createEmptyMap(self.mapSize)
        self.vtilemap_example = VTileTerrainGenerator.placeStartingPoint(self.vtilemap_example, VTileTerrainGenerator.loadBaseBiomes()[0])
        self.vtile_timer = 0 """

        """ self.tile_width = WIDTH/len(self.vtilemap_example[0])
        self.tile_height = HEIGHT/len(self.vtilemap_example)

        self.draw_screen = pg.Surface((WIDTH, HEIGHT))
        self.drawn = False """

    def render_examples(self):
        """ fp = flatpane("img", self.sprites, sprite="atmo", position=(100, 100))
        self.to_render.append(RenderItem("sprite", 5, {"sprite":fp.sprite, "rect":(100, 100, 100, 100)})) """

        """ self.vui_example.metadata["rect"].x, self.vui_example.metadata["rect"].y = self.mouse_info[0]
        self.to_render.append(self.vui_example) """

        """ for i in range(1):
            bruh = RenderItem("poly", 4, {"width":0, "points":[(0, 100), (100, 0), (200, 100), (300, 0), (400, 100), (200, 400)], "color":red})
            self.to_render.append(bruh)
            ili = RenderItem("poly", 2, {"width":0, "points":[(0, 0), (0, 400), (400, 400), (400, 0)], "color":lmagenta})
            self.to_render.append(ili)
            dolni = RenderItem("circle", 3, {"center":(200, 200), "radius":(200), "color":orange})
            self.to_render.append(dolni) """
        """ heh = RenderItem("text", 5, {"no_bg":True, "font":("Arial", 120), "color":cyan, "text":str(round(self.clock.get_fps()))})
        Datablock.render_data.append(heh) """
        """ self.to_render.append(RenderItem("sprite", 4, {"sprite":self.sprites["atmo"], "rect":[pg.mouse.get_pos()[0]+random.randint(0, 240), pg.mouse.get_pos()[1]+random.randint(0, 240), WIDTH, HEIGHT]})) """

        """ self.vtile_timer += self.dt
        if self.vtile_timer >= .1:
            self.vtile_timer = 0
            try:
                #self.vtilemap_example = VTileGenerator.propagateNextStep(self.vtilemap_example)[0]
                #self.vtilemap_example = VTileGenerator.propagateNextStepFullchance(self.vtilemap_example)[0]
                self.vtilemap_example, nic, overlayMap = VTileTerrainGenerator.propagateNextStep(self.vtilemap_example, VTileTerrainGenerator.loadBaseBiomes(), baseBiomeWeights, 5) # 1 - chaos, 7 - grass
            except: pass """

        """ for y in range(len(self.vtilemap_example)):
            for x in range(len(self.vtilemap_example[y])):
                if self.vtilemap_example[y][x] != -1:
                    self.to_render.append(RenderItem("rect", 3, {"rect":(x*(self.tile_width), y*self.tile_height, self.tile_width, self.tile_height), "color":self.color_examples[self.vtilemap_example[y][x]]})) """
        
        """ if not self.drawn:
            for y in range(len(self.vtilemap_example)):
                for x in range(len(self.vtilemap_example[y])):
                    if self.vtilemap_example[y][x] != -1:
                        pg.draw.rect(self.draw_screen, self.color_examples[self.vtilemap_example[y][x]], pg.Rect(x*self.tile_width, y*self.tile_height, self.tile_width, self.tile_height))
            self.drawn = True """

        """ draw_buffer = VTileTerrainGenerator.createEmptyMap(self.mapSize)
        try:
            for rewrite in overlayMap:
                draw_buffer[rewrite[0]][rewrite[1]] = rewrite[2]

            overlayMap.clear()

            for y in range(len(draw_buffer)):
                for x in range(len(draw_buffer[y])):
                    if draw_buffer[y][x] != -1:
                        pg.draw.rect(self.draw_screen, self.color_examples[draw_buffer[y][x]], pg.Rect(x*(self.tile_width), y*self.tile_height, self.tile_width, self.tile_height))
        except:pass """
        """ self.draw("sprite", 3, {"rect":(0, 0, WIDTH, HEIGHT), "sprite":self.draw_screen}) """

    def render_fps(self):
        
        self.draw("text", self.LAYER_UI_TOP, {"no_bg":True, "font":self.default_font, "color":white, "text":str(int(self.clock.get_fps()))})

    def do_physics(self):
        pass
                        
    def load_sounds(self):
        pass

    def render(self):
        if MULTITHREADED_RENDERING:
            # set caption
            try:
                pg.display.set_caption(f"{self.name}: ({int(self.clock.get_fps())} UPS / {int(self.renderer.clock.get_fps())} FPS)")
            except: pass

            # update full render data
            with self.thread_lock:
                self.to_render_full = self.to_render.copy()

            # render last updated window with opengl
            if OGL_ENABLED: # such a stupid implementation >:(
                with self.thread_lock:
                    self.ogl_handler.frame_tex = self.ogl_handler.surf_to_tex(self.window)
                self.ogl_handler.frame_tex.use(0)
                self.ogl_handler.program["tex"] = 0
                self.ogl_handler.render_object.render(mode=mgl.TRIANGLE_STRIP)
                
                pg.display.flip()

                self.ogl_handler.frame_tex.release()




        else:
            pg.display.set_caption(f"{self.name}: ({int(self.clock.get_fps())} FPS)")

            self.renderer.render(self.to_render)

    def draw(self, itemType:str, layer:int, metadata:dict):
        self.to_render.append(RenderItem(itemType, layer, metadata)) # autotransfers metadata into ## haha idk what was supposed to be here

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False

        self.keyhandler.update_keys()

    def update(self):
        self.to_render.clear()
        self.dt = self.clock.tick(FPS_LOGIC_LIMIT) / 1000

        # refresh mouse information
        mouse_pressed = pg.mouse.get_pressed()

        left_pressed = mouse_pressed[0]

        mouse_changed = (left_pressed != self.mouse_last)

        self.mouse_last = left_pressed

        self.mouse_info = (pg.mouse.get_pos(), left_pressed, mouse_changed)
        self.corrected_mouse_info = (self.screen_to_game_coords(pg.mouse.get_pos()), left_pressed, mouse_changed)

        #self.draw("circle", 9, {"center":self.corrected_mouse_info[0]})

        # do main game logic
        self.do_logic()

        # update and render active scene
        self.scene_handler.updateScene()
        self.scene_handler.renderScene()

        # post frame stuff
        self.render_fps()
        self.collect_logs()
        self.print_log() # print and clear log of current cycle

    def do_logic(self): # all non-engine related logic should go here
        pass
        """ self.animations["example_anim"].anim_pos = (self.mouse_info[0][0], self.mouse_info[0][1])

        self.animations_to_render.append("example_anim") """
 
    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.animation_handler.render_animations()
            self.render()
        pg.quit()
        sys.exit()

def runGame():
    global app
    app = MainEngine()
    app.run()