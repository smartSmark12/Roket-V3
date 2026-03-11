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
from game.scripts.alarm import Alarm
from game.scripts.ui_frame_builder import UIFrameBuilder
from game.scripts.sprite_window import SpriteWindow
from scripts.core.settings import GAME_NAME, DEFAULT_SCENE_NAME
from game.scripts.roket_body_related.roket_body import RoketBody
from game.scripts.roket_body_related.roket_module import RoketModule # load modules from json file configs
from game.scripts.roket_body_related.roket_module_slot import RoketModuleSlot
from game.scripts.spawnnable_object import SpawnableObject
from game.scripts.spawnable_navigator import Navigator
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

        # load user settings
        self.load_settings()

        self.create_resolutions()
        self.set_resolution()
        self.create_draw_window()

        ## need to redo this part
        #if IN_FULLSCREEN:
        if self.user_fullscreen:
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
        self.to_scale = self.sprite_handler.to_scale

        # logger setup
        self.create_runtime_logger()

        ## mouse last pressed status?? Why here?
        self.mouse_last = 0

    # write your game on_init here
    def game_on_init(self):
        # set render layers
        self.LAYER_UI_BOTTOM = 7
        self.LAYER_TITLE_PLANETS = 4 # actually just a reference - animations take only numbers from animations_to_create.py

        # alarms setup
        self.alarms = {}

        self.title_planet_alarm = self.add_alarm("planet_spawn", TITLE_PLANET_SPAWNING_PERIOD, self.spawn_title_planets, True)

        # assign empty corrected mouse info
        self.corrected_mouse_info = None

        # load fonts # can hardcode, cause you'll still need to relaunch the game to take effect
        self.h1_font = pg.Font(DEFAULT_FONT_PATH, int(H1_FONT_SIZE * (self.height / HEIGHT)))
        self.button_font = pg.Font(DEFAULT_FONT_PATH, int(BUTTON_FONT_SIZE * (self.height / HEIGHT)))
        self.version_font = pg.Font(DEFAULT_FONT_PATH, int(VERSION_FONT_SIZE * (self.height / HEIGHT)))
        self.mode_font = pg.Font(DEFAULT_FONT_PATH, int(GAMEMODE_FONT_SIZE * (self.height / HEIGHT)))

        # load localization
        #self.localization_code = DEFAULT_LOCALIZATION_CODE ## temp
        self.load_localization()

        # load keybinds
        self.keybind_path = DEFAULT_KEYBIND_PATH ## also temp
        self.load_keybinds()

        # load roket bodies and modules
        self.load_spawnables()
        self.load_roket_module_types()
        self.load_roket_modules()
        self.load_roket_bodies()

        # create darker button variants
        BUTTON_COLOR_SUBTRACT_COLOR = (30, 30, 30)
        for sprite in ["button_template", "button_template_vertical", "mainmenu_settings_button", "mainmenu_leaderboard_button"]:
            dark_name = sprite+"_dark"
            self.sprites[dark_name] = self.sprites[sprite].copy()
            pg.Surface.fill(self.sprites[dark_name], BUTTON_COLOR_SUBTRACT_COLOR, special_flags=pg.BLEND_SUB)

        # black&white mode variants ## omg this fuckass method is gonna be the end of me
        #TINT_COLOR = (33/4, 158/4, 188/4)
        for sprite in ["button_mode_career", "button_mode_infinite", "button_mode_dummy"]:
            baw_name = sprite+"_baw"

            sprite_out:pg.Surface = self.sprites[sprite].copy()

            for y in range(sprite_out.get_height()):
                for x in range(sprite_out.get_width()):
                    pix_col = sprite_out.get_at((x,y))
                    baw_val = pix_col.r + pix_col.g + pix_col.b# / 3)
                    baw_col = pg.Color(baw_val)
                    sprite_out.set_at((x,y), baw_col)

            #sprite_out.fill(TINT_COLOR, None, pg.BLEND_RGBA_ADD)

            self.sprites[baw_name] = sprite_out # its not baw and likely alpha blending, but fk it we ball it looks okay enough

        # planet movement speed
        self.planet_movement_speed = [16,9] # px/s

        # gamemode select preset
        self.selected_mode = "mode_career"

        # active ship
        self.active_ship_name = "legacy" # will be replaced by loading a save perhaps?

        # rocket config select
        #self.selected_roket_body = self.roket_bodies["legacy"]

        # add all scenes
        self.scene_handler.addScene(Scene(self, "title"))               # the main game title
        self.scene_handler.addScene(Scene(self, "main_menu"))           # main menu - root point
        self.scene_handler.addScene(Scene(self, "ship_modification"))   # upgrades, types, modification
        self.scene_handler.addScene(Scene(self, "game"))                # actual game scene
        self.scene_handler.addScene(Scene(self, "career"))              # career overview and level select
        self.scene_handler.addScene(Scene(self, "infinite_setup"))      # select music and level for endless mode
        self.scene_handler.addScene(Scene(self, "achievements"))        # achievement and game stats overview
        self.scene_handler.addScene(Scene(self, "settings"))            # resolution, language, etc. settings

        # set main scene
        self.scene_handler.setActiveScene("title")

        title_scene = self.scene_handler.getScene("title")
        main_menu_scene = self.scene_handler.getScene("main_menu")
        ship_mod_scene = self.scene_handler.getScene("ship_modification")
        game_scene = self.scene_handler.getScene("game")
        career_scene = self.scene_handler.getScene("career")
        infinite_setup_scene = self.scene_handler.getScene("infinite_setup")
        achievements_scene = self.scene_handler.getScene("achievements")
        settings_scene = self.scene_handler.getScene("settings")

        # override scene updates
        title_scene.update = self.title_update
        main_menu_scene.update = self.main_menu_update
        ship_mod_scene.update = self.ship_modification_update

        # override scene renders
        title_scene.render = self.title_render
        main_menu_scene.render = self.main_menu_render
        ship_mod_scene.render = self.ship_modification_render

        # override scene shis

        title_button_width = 280
        title_button_height = 128

        title_square_button_size = 128
        title_side_button_x_distance = 250
        title_button_y_offset = 160 # not sure why this cant be the same as button x dist ::

        main_menu_button_start_y = 750 # all values autoconverted by to_scale_x/y
        main_menu_button_width = title_button_width
        main_menu_button_height = title_button_height
        main_menu_button_y_offset = title_button_y_offset

        main_menu_background_frame_width = 1600
        main_menu_background_frame_height = 600
        main_menu_background_frame_x = (WIDTH - main_menu_background_frame_width) / 2
        main_menu_background_frame_y = 100

        main_menu_background_frame_width_part = main_menu_background_frame_width / 10
        main_menu_background_frame_margin = 20

        main_menu_ship_frame_width = main_menu_background_frame_width_part * 5 - 2 * main_menu_background_frame_margin
        main_menu_mode_frame_width = main_menu_background_frame_width_part * 3 - 2 * main_menu_background_frame_margin
        main_menu_news_frame_width = main_menu_background_frame_width_part * 2 - 2 * main_menu_background_frame_margin

        main_menu_ship_frame_x = main_menu_background_frame_x + main_menu_background_frame_margin
        main_menu_mode_frame_x = main_menu_ship_frame_x + main_menu_ship_frame_width + 2 * main_menu_background_frame_margin
        main_menu_news_frame_x = main_menu_mode_frame_x + main_menu_mode_frame_width + 2 * main_menu_background_frame_margin

        ## title

        title_scene.main_text = self.texts["title_title"]
        title_scene.version_text = "v" + GAME_VERSION + " - " + GAME_VERSION_HINT
        title_scene.play_text = self.texts["title_play"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_forward")
        title_scene.exit_text = self.texts["title_exit"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_back")
        title_scene.buttons = {}
        title_scene.planets = []

        ## main_menu
        main_menu_scene.launch_text = self.texts["main_menu_launch"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_forward")
        main_menu_scene.return_text = self.texts["main_menu_return"] + " " + self.get_keybind_keycode_name_in_square_brackets("ui_back")
        main_menu_scene.background_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(main_menu_background_frame_width), self.to_scale_y(main_menu_background_frame_height), self.sprites)
        main_menu_scene.background_frame_pos = (main_menu_background_frame_x, main_menu_background_frame_y)
        main_menu_scene.ship_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(main_menu_ship_frame_width), self.to_scale_y(main_menu_background_frame_height), self.sprites)
        main_menu_scene.ship_frame_pos = (main_menu_ship_frame_x, main_menu_background_frame_y)
        main_menu_scene.mode_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(main_menu_mode_frame_width), self.to_scale_y(main_menu_background_frame_height), self.sprites)
        main_menu_scene.mode_frame_pos = (main_menu_mode_frame_x, main_menu_background_frame_y)
        main_menu_scene.news_frame = UIFrameBuilder.get_ui_frame(self.to_scale_x(main_menu_news_frame_width), self.to_scale_y(main_menu_background_frame_height), self.sprites)
        main_menu_scene.news_frame_pos = (main_menu_news_frame_x, main_menu_background_frame_y)
        main_menu_scene.buttons = {}

        ### ship frame
        ship_window_size_mult = 0.4
        ship_window_size = (main_menu_ship_frame_width * ship_window_size_mult, main_menu_ship_frame_width * ship_window_size_mult)
        ship_window_pos = (main_menu_ship_frame_x + (main_menu_ship_frame_width - ship_window_size[0]) / 2, main_menu_background_frame_y + (main_menu_background_frame_height - ship_window_size[1]) / 2 - 50) # ja uz asi nedavam matiku pls proc 4 a ne 2
        main_menu_scene.ship_window = SpriteWindow(self, self.get_active_ship().sprites.get_sprite(0), ship_window_pos, ship_window_size, self.LAYER_UI_TOP)

        ship_switch_size = (128, 280)
        ship_switch_left_button_pos = (main_menu_ship_frame_x + 30, main_menu_background_frame_y + (main_menu_background_frame_height - ship_switch_size[1]) / 2)
        ship_switch_right_button_pos = (main_menu_ship_frame_x - 30 + main_menu_ship_frame_width - ship_switch_size[0], main_menu_background_frame_y + (main_menu_background_frame_height - ship_switch_size[1]) / 2)

        ship_mod_button_size = (main_menu_button_width, main_menu_button_height)
        ship_mod_button_pos = (main_menu_ship_frame_x + (main_menu_ship_frame_width - ship_mod_button_size[0]) / 2, main_menu_background_frame_y + 420)

        main_menu_scene.buttons["ship_switch_left"] = button(flatpane("sprite", {"main":self.sprites["button_template_vertical"], "hover":self.sprites["button_template_vertical_dark"]}, sprite="main"), pg.Rect(self.to_scale(ship_switch_left_button_pos), self.to_scale(ship_switch_size)), 0, None, partial(self.cycle_main_menu_ship, direction=0), None, self)
        main_menu_scene.buttons["ship_switch_right"] = button(flatpane("sprite", {"main":self.sprites["button_template_vertical"], "hover":self.sprites["button_template_vertical_dark"]}, sprite="main"), pg.Rect(self.to_scale(ship_switch_right_button_pos), self.to_scale(ship_switch_size)), 0, None, partial(self.cycle_main_menu_ship, direction=1), None, self)
        main_menu_scene.buttons["ship_modification"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale(ship_mod_button_pos), self.to_scale(ship_mod_button_size)), 0, None, partial(self.scene_handler.setActiveScene, "ship_modification"), None, self)

        main_menu_scene.ship_name_text = self.get_active_ship().get_property("displayName")
        main_menu_scene.ship_name_text_center = (main_menu_ship_frame_x + main_menu_ship_frame_width / 2, main_menu_background_frame_y + self.to_scale_y(50))

        main_menu_scene.left_switch_text = self.texts["main_menu_switch_left"]
        main_menu_scene.right_switch_text = self.texts["main_menu_switch_right"]
        main_menu_scene.mod_button_text = self.texts["main_menu_ship_modification"]

        ### gamemode frame
        mode_button_size = (360, 146)
        mode_button_margin = 40
        mode_button_start_pos = (main_menu_mode_frame_x + mode_button_margin, main_menu_background_frame_y + mode_button_margin)
        main_menu_scene.buttons["mode_career"] = button(flatpane("sprite", {"main":self.sprites["button_mode_career_baw"], "hover":self.sprites["button_mode_career"]}, sprite="main"), pg.Rect(self.to_scale(mode_button_start_pos), self.to_scale(mode_button_size)), 0, None, partial(self.change_gamemode, "mode_career"), None, self)
        main_menu_scene.buttons["mode_infinite"] = button(flatpane("sprite", {"main":self.sprites["button_mode_infinite_baw"], "hover":self.sprites["button_mode_infinite"]}, sprite="main"), pg.Rect(self.to_scale((mode_button_start_pos[0], mode_button_start_pos[1] + mode_button_size[1] + mode_button_margin)), self.to_scale(mode_button_size)), 0, None, partial(self.change_gamemode, "mode_infinite"), None, self)
        main_menu_scene.buttons["mode_dummy"] = button(flatpane("sprite", {"main":self.sprites["button_mode_dummy_baw"], "hover":self.sprites["button_mode_dummy"]}, sprite="main"), pg.Rect(self.to_scale((mode_button_start_pos[0], mode_button_start_pos[1] + 2 * mode_button_size[1] + 2 * mode_button_margin)), self.to_scale(mode_button_size)), 0, None, partial(self.change_gamemode, "mode_dummy"), None, self)

        main_menu_scene.mode_button_names = ["mode_career", "mode_infinite", "mode_dummy"]

        main_menu_scene.mode_texts = {}
        main_menu_scene.mode_texts["mode_career"] = self.texts["main_menu_mode_career"]
        main_menu_scene.mode_texts["mode_infinite"] = self.texts["main_menu_mode_infinite"]
        main_menu_scene.mode_texts["mode_dummy"] = self.texts["main_menu_mode_dummy"]

        ## create all title buttons
        title_scene.buttons["play"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_button_width) / 2), self.to_scale_y((HEIGHT - title_button_height) / 2 + title_button_y_offset), self.to_scale_x(title_button_width), self.to_scale_y(title_button_height)), 0, None, partial(self.scene_handler.setActiveScene, "main_menu"), None, self)
        title_scene.buttons["exit"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_button_width) / 2), self.to_scale_y((HEIGHT - title_button_height) / 2 + 2 * title_button_y_offset), self.to_scale_x(title_button_width), self.to_scale_y(title_button_height)), 0, None, partial(self.exit_game), None, self)
        
        title_scene.buttons["settings"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_settings_button"], "hover":self.sprites["mainmenu_settings_button_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_square_button_size) / 2 - title_side_button_x_distance), self.to_scale_y((HEIGHT - title_square_button_size) / 2 + title_button_y_offset), self.to_scale_x(title_square_button_size), self.to_scale_y(title_square_button_size)), 0, None, partial(print, "options pressed"), None, self)
        title_scene.buttons["achievements"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_leaderboard_button"], "hover":self.sprites["mainmenu_leaderboard_button_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - title_square_button_size) / 2 + title_side_button_x_distance), self.to_scale_y((HEIGHT - title_square_button_size) / 2 + title_button_y_offset), self.to_scale_x(title_square_button_size), self.to_scale_y(title_square_button_size)), 0, None, partial(print, "achievements pressed"), None, self)

        ## create all main_menu buttons
        main_menu_scene.buttons["launch"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - main_menu_button_width) / 2), self.to_scale_y(main_menu_button_start_y), self.to_scale_x(main_menu_button_width), self.to_scale_y(main_menu_button_height)), 0, None, partial(self.launch_from_main_menu), None, self)
        main_menu_scene.buttons["return"] = button(flatpane("sprite", {"main":self.sprites["button_template"], "hover":self.sprites["button_template_dark"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - main_menu_button_width) / 2), self.to_scale_y(main_menu_button_start_y + main_menu_button_y_offset), self.to_scale_x(main_menu_button_width), self.to_scale_y(main_menu_button_height)), 0, None, partial(self.scene_handler.setActiveScene, "title"), None, self)

        ## ship modification



    def create_resolutions(self):
        # set possible resolutions
        self.RESOLUTIONS = [
            (640, 360),
            (1280, 720),
            (1920, 1080),
            (2560, 1440),
            (3840, 2160),
            tuple(self.user_resolution) # loaded resolution here; converted to tuple for compatibility
        ] 

        """ (1280, 960),
            (1440, 1080),
            (80,45),
            (1200, 400) """
        
        print(self.RESOLUTIONS)

    def set_resolution(self):
        #self.active_resolution_index =  self.DEBUG_RESOLUTION_INDEX#4
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

        # debug
        print(f"{__name__}: loaded localization: {self.localization_code}")

    def load_spawnables(self):
        self.roket_spawnables = {}

        loaded_spawnables = JsonLoader.load_from_file(DEFAULT_ROKET_SPAWNABLE_PATH)

        for spawnable_name, spawnable in loaded_spawnables["spawnables"].items():

            # prepare sprites
            loaded_sprite_paths = spawnable["animation_sprites"]

            # prepare prefix
            sprite_path_prefix = None

            if spawnable["sprite_source"] == "internal":
                sprite_path_prefix = INTERNAL_SPRITE_PATH
            elif spawnable["sprite_source"] == "external":
                sprite_path_prefix = EXTERNAL_SPRITE_PATH
            else:
                sprite_path_prefix = "" # when using fully custom paths

            # output sprite dict
            sprite_dict = {}

            # load sprites
            for sprite_index in range(len(loaded_sprite_paths)):
                sprite_path = sprite_path_prefix + loaded_sprite_paths[sprite_index]

                # generate sprite name
                sprite_name = f"{spawnable_name}_anim_{sprite_index}"

                sprite_dict[sprite_index] = self.sprite_handler.load_sprite(sprite_name, sprite_path, (100,100), "ca")


            # create final flatpane
            spawnable_sprite = flatpane("sprite", sprite_dict, sprite=0)

            # collider
            collision_rect = pg.Rect(
                0,
                0,
                spawnable["collider_size"][0],
                spawnable["collider_size"][1]
            )

            navigator = Navigator(spawnable["navigator"])

            # spawnable
            self.roket_spawnables[spawnable_name] = SpawnableObject(
                name=spawnable_name,
                displayName=spawnable["display_name"],
                collider=collision_rect,
                sprites=spawnable_sprite,
                navigator=navigator,
                actions=spawnable["actions"]
            )

        print("--------\nLoaded spawnables:\n")

        for spawnable_name, spawnable in self.roket_spawnables.items():
            print(f"{spawnable.displayName} ({spawnable.name})")

        print("")

    def load_roket_module_types(self):
        self.roket_module_types = []

        loaded_module_types = JsonLoader.load_from_file(DEFAULT_ROKET_MODULE_TYPE_PATH)

        for module_type in loaded_module_types["ship_module_types"]:
            if module_type not in self.roket_module_types:
                self.roket_module_types.append(module_type)
            else:
                print(f"{__name__}:module_type_loader: module type {module_type} already loaded; skipping")

        print("--------\nLoaded module types:\n")

        for module_type in self.roket_module_types:
            print(module_type)

        print("") # sep

    def load_roket_modules(self): # need to make safe!
        self.roket_modules = {}

        loaded_modules = JsonLoader.load_from_file(DEFAULT_ROKET_MODULE_PATH)

        for module_name, module in loaded_modules["ship_modules"].items():

            # prepare sprites
            loaded_sprite_path = module["sprite"]

            # prepare prefix
            sprite_path_prefix = None

            if module["sprite_source"] == "internal":
                sprite_path_prefix = INTERNAL_SPRITE_PATH
            elif module["sprite_source"] == "external":
                sprite_path_prefix = EXTERNAL_SPRITE_PATH
            else:
                sprite_path_prefix = "" # when using fully custom paths

            sprite_path = sprite_path_prefix + loaded_sprite_path

            # generate sprite name
            sprite_name = f"{module_name}_module"

            sprite = self.sprite_handler.load_sprite(sprite_name, sprite_path, (100,100), "ca")

            module_sprite = flatpane("sprite", {"main":sprite}, sprite="main")

            self.roket_modules[module_name] = RoketModule(
                                                            module_name,
                                                            module["display_name"],
                                                            module["module_type"],
                                                            1,
                                                            1,
                                                            module["modifiers"],
                                                            module_sprite
                                                        )
            
        print("--------\nLoaded modules:\n")

        for module_name, module in self.roket_modules.items():
            print(f"{module.displayName} ({module.name}; {module.modType})")

        print("")

    def load_roket_bodies(self): # need to make safe!
        self.roket_bodies = {}

        loaded_bodies = JsonLoader.load_from_file(DEFAULT_ROKET_BODY_PATH)

        for body_name in loaded_bodies["ship_bodies"]:
            body = loaded_bodies["ship_bodies"][body_name]

            # prepare sprites
            loaded_sprite_paths = body["animation_sprites"]

            # prepare prefix
            sprite_path_prefix = None

            if body["sprite_source"] == "internal":
                sprite_path_prefix = INTERNAL_SPRITE_PATH
            elif body["sprite_source"] == "external":
                sprite_path_prefix = EXTERNAL_SPRITE_PATH
            else:
                sprite_path_prefix = "" # when using fully custom paths

            # output sprite dict
            sprite_dict = {}

            # load sprites
            for sprite_index in range(len(loaded_sprite_paths)):
                sprite_path = sprite_path_prefix + loaded_sprite_paths[sprite_index]

                # generate sprite name
                sprite_name = f"{body_name}_anim_{sprite_index}"

                sprite_dict[sprite_index] = self.sprite_handler.load_sprite(sprite_name, sprite_path, (100,100), "ca")


            # create final flatpane
            body_sprite = flatpane("sprite", sprite_dict, sprite=0)

            # load module slots
            loaded_slots = body["module_slots"]

            # prepare module slots
            module_slots = {}

            # create modules
            for slot_id_str in loaded_slots:
                loaded_slot = loaded_slots[slot_id_str]
                slot_id = None
                try:
                    slot_id = int(slot_id_str)
                except:
                    print("smula ig")
                    continue
                
                slot = None

                try:
                    slot = RoketModuleSlot(
                                            slotId=slot_id,
                                            name=loaded_slot["name"],
                                            allowedModuleTypes=loaded_slot["allowed_module_types"]
                                        ) # modules have to be loaded later from a save
                    
                    module_slots[slot_id] = slot

                except:
                    print("bad luck ~ Yoru")
                    continue

            # create collider
            collision_rect = pg.Rect(
                0,
                0,
                body["collider_size"][0],
                body["collider_size"][1]
            )

            collision_rect.center = body["collider_offset"]

            # build final ship body ## BODIES DO NOT EXPLICITLY SAVE ACTIVE MODULES IN SLOTS - saved in game/hangar saves
            self.roket_bodies[body_name] = RoketBody(
                                                    name=body_name,
                                                    displayName=body["display_name"],
                                                    baseLives=body["base_lives"],
                                                    baseSprites=body_sprite,
                                                    position=(0, 0),
                                                    size=body["size"],
                                                    collisionRect=collision_rect,
                                                    moduleSlots=module_slots
                                                    )

        print("--------\nLoaded ships:\n")

        for ship_name, ship in self.roket_bodies.items():
            print(f"{ship.get_property("displayName")} ({ship.name})")

        print("")

    def load_keybinds(self):
        loaded_keybinds = JsonLoader.load_from_file(DEFAULT_KEYBIND_PATH)

        self.keyhandler.keybinds = loaded_keybinds

        self.keyhandler.update_keybind_buffers()

        #print(loaded_keybinds)

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

    def render_version_info(self):
        self.draw("text", self.LAYER_UI_TOP, {"text":self.scene_handler.getScene("title").version_text, "no_bg":True, "font":self.version_font, "rect":pg.Rect(self.to_scale_x(30), self.to_scale_y(HEIGHT - 50), 0, 0), "color":gray})

    def change_gamemode(self, gameModeName:str):
        self.selected_mode = gameModeName

    def launch_from_main_menu(self):
        match self.selected_mode:
            case "mode_career":
                self.scene_handler.setActiveScene("career")

            case "mode_infinite":
                self.scene_handler.setActiveScene("infinite_setup")

            case "mode_dummy":
                print("dummy launch!")

    def cycle_main_menu_ship(self, direction:bool):
        active_ship_name = self.active_ship_name
        ship_names = list(self.roket_bodies.keys())

        active_ship_name_index = ship_names.index(active_ship_name)

        if direction:
            active_ship_name_index += 1
        else:
            active_ship_name_index -= 1

        if active_ship_name_index < 0:
            active_ship_name_index = len(ship_names) - 1
        elif active_ship_name_index > len(ship_names) - 1:
            active_ship_name_index = 0

        self.set_active_ship(ship_names[active_ship_name_index])
        
    def set_active_ship(self, shipName:str):
        ship_names = list(self.roket_bodies.keys())

        if shipName not in ship_names:
            print("ship not found ig?")
        
        else:
            self.active_ship_name = shipName
            print(f"{shipName} set as active ship")

            # udpate ship window
            self.scene_handler.getScene("main_menu").ship_window.set_sprite(self.sprites.get(f"{shipName}_anim_0"))
            self.scene_handler.getScene("main_menu").ship_name_text = self.get_active_ship().get_property("displayName")

    def get_active_ship(self) -> RoketBody:
        return self.roket_bodies.get(self.active_ship_name)

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

        # planet movement
        for planet in title.planets:
            self.animations[planet].anim_pos = (
                                                self.animations[planet].anim_pos[0] - self.to_scale_x(self.planet_movement_speed[0])*self.dt,
                                                self.animations[planet].anim_pos[1] - self.to_scale_y(self.planet_movement_speed[1])*self.dt
                                                )
            
            if self.animations[planet].anim_pos[0] < -200:
                self.animation_handler.remove_animation(planet)
                title.planets[title.planets.index(planet)] = None

        title.planets = [i for i in title.planets if i is not None]

    def title_render(self):
        title = self.scene_handler.getScene("title")

        # draw title
        self.draw("text", self.LAYER_UI_TOP, {"text":title.main_text, "no_bg":True, "font":self.h1_font, "center":(self.width/2, self.height/5 * 1.5)})

        # draw version info
        self.render_version_info()

        # draw button texts
        self.draw_button_text(title.play_text, title.buttons["play"])
        self.draw_button_text(title.exit_text, title.buttons["exit"])

        for button in title.buttons:
            title.buttons[button].render()

        # planet render
        for planet in title.planets:
            self.animations_to_render.append(planet)


        # debug
        #self.draw("sprite", 7, {"sprite":UIFrameBuilder.get_ui_frame(400, 300, self.sprites), "rect":(100, 100, 0, 0)})

    def main_menu_update(self):
        main_menu = self.scene_handler.getScene("main_menu")

        # update all buttons
        for button_index in main_menu.buttons:
            button = main_menu.buttons[button_index]
            button.activation_detection(self.corrected_mouse_info)
            button.update_hold_time(self.corrected_mouse_info)

        # change button sprite to colored when active ## has to be after updating button interactions
        for button_name in main_menu.mode_button_names:
            button = main_menu.buttons[button_name]

            if self.selected_mode == button_name:
                button.set_active_sprite("hover")

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
        self.draw_button_text(main_menu.left_switch_text, main_menu.buttons["ship_switch_left"])
        self.draw_button_text(main_menu.right_switch_text, main_menu.buttons["ship_switch_right"])
        self.draw_button_text(main_menu.mod_button_text, main_menu.buttons["ship_modification"])

        # draw background frame
        #self.draw("sprite", self.LAYER_UI_BOTTOM, {"sprite":main_menu.background_frame, "rect":(self.to_scale_x(main_menu.background_frame_pos[0]), self.to_scale_y(main_menu.background_frame_pos[1]), 0, 0)})
        self.draw("sprite", self.LAYER_UI_BOTTOM, {"sprite":main_menu.ship_frame, "rect":(self.to_scale_x(main_menu.ship_frame_pos[0]), self.to_scale_y(main_menu.ship_frame_pos[1]), 0, 0)})
        self.draw("sprite", self.LAYER_UI_BOTTOM, {"sprite":main_menu.mode_frame, "rect":(self.to_scale_x(main_menu.mode_frame_pos[0]), self.to_scale_y(main_menu.mode_frame_pos[1]), 0, 0)})
        self.draw("sprite", self.LAYER_UI_BOTTOM, {"sprite":main_menu.news_frame, "rect":(self.to_scale_x(main_menu.news_frame_pos[0]), self.to_scale_y(main_menu.news_frame_pos[1]), 0, 0)})

        # draw ship frame
        main_menu.ship_window.render()

        # draw ship name text
        self.draw("text", self.LAYER_UI_TOP, {"text":main_menu.ship_name_text, "font":self.button_font, "center":main_menu.ship_name_text_center, "no_bg":True, "rect":pg.Rect(0,0,0,0), "color":black}) # idk maybe white

        """ main_menu.ship_button_left.render() """

        # draw buttons
        for button in main_menu.buttons:
            main_menu.buttons[button].render()

        # draw mode button texts
        for button_name in main_menu.mode_button_names:
            button = main_menu.buttons[button_name]

            if not (button.is_hovered(self.mouse_info[0]) or self.selected_mode == button_name):
                self.draw("text", self.LAYER_UI_TOP, {"text":main_menu.mode_texts[button_name], "font":self.mode_font, "center":button.rect.center, "color":white, "no_bg":True})

        # draw version info
        self.render_version_info()

    def ship_modification_update(self):
        pass

    def ship_modification_render(self):
        pass

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
    
    def spawn_title_planets(self):

        if random.randint(0, TITLE_PLANET_SPAWNING_ANICHANCE) == 0:

            planet_name_prefix = "title_planet_"
            animation_number = 0

            while planet_name_prefix + str(animation_number) in self.animations:
                animation_number += 1
            
            x_pos = 100
            y_pos = 100

            while self.in_bounds((x_pos, y_pos)):
                x_pos = random.randint(int(WIDTH/2), WIDTH)
                y_pos = random.randint(int(HEIGHT/2), HEIGHT)

            self.animation_handler.add_animation(planet_name_prefix + str(animation_number), ["title_planet_0_0","title_planet_0_1","title_planet_0_2"], 2, self.LAYER_TITLE_PLANETS, (self.to_scale_x(x_pos), self.to_scale_y(y_pos)))
            self.scene_handler.getScene("title").planets.append(planet_name_prefix + str(animation_number))

    def in_bounds(self, pos): # this thing is lowkey crazy :(( ## its worldspace, NOT SCREENSPACE
        x = pos[0]
        y = pos[1]

        if x > 0 and y > 0 and x < WIDTH and y < HEIGHT:
            return True
        else:
            return False

    def update_alarms(self):
        for alarm in self.alarms:

            if self.alarms[alarm].getRemoveSchedule():
                del self.alarms[alarm] # idk

            self.alarms[alarm].checkTimeout(self.dt)

    def pause_alarm(self, alarmId:str):
        self.alarms[alarmId].pauseAlarm()

    def unpause_alarm(self, alarmId:str):
        self.alarms[alarmId].unpauseAlarm()

    def add_alarm(self, alarmName:str, alarmTime:int|float, timeoutFunction, repeatAlarm:bool) -> int:
        alarm = Alarm(alarmName, alarmTime, timeoutFunction, repeatAlarm)
        self.alarms[id(alarm)] = alarm

        return id(alarm)

    def remove_alarm(self, alarmId:str|int):
        self.alarms[alarmId].removeAlarm()

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

    def load_settings(self):
        settings_read = None

        # try loading user settings        
        settings_read = JsonLoader.load_from_file(ACTIVE_SETTINGS_PATH)

        # load defaults if no settings file exists
        if not settings_read:
            settings_read = JsonLoader.load_from_file(DEFAULT_SETTINGS_PATH)
            print("loaded default settings! Something's probably gone wrong :>")

        #print(settings_read)

        # apply settings
        self.user_resolution = settings_read["resolution"]
        self.user_fullscreen = settings_read["fullscreen"]
        self.user_fps_limit = settings_read["fps_limit"]

        self.active_resolution_index = 5 # uhhh changeme

        self.localization_code = settings_read["localization"]

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
        self.dt = self.clock.tick(self.user_fps_limit) / 1000

        # refresh mouse information
        mouse_pressed = pg.mouse.get_pressed()

        left_pressed = mouse_pressed[0]

        mouse_changed = (left_pressed != self.mouse_last)

        self.mouse_last = left_pressed

        self.mouse_info = (pg.mouse.get_pos(), left_pressed, mouse_changed)

        ## correct mouse information for different resolutions
        self.corrected_mouse_info = (self.screen_to_game_coords(pg.mouse.get_pos()), left_pressed, mouse_changed)

        #self.draw("circle", 9, {"center":self.corrected_mouse_info[0]})

        # update alarms
        self.update_alarms()

        # do main game logic
        self.do_logic()

        # update and render active scene
        self.scene_handler.updateScene()
        self.scene_handler.renderScene()

        # post frame stuff
        self.render_fps()
        self.collect_logs()
        self.print_log() # print and clear log of current cycle

    def do_logic(self): # all non-engine related logic should go here (unless you use scenes ofc)
        # pause planet spawning alarm if title not active
        if self.scene_handler.getActiveSceneName() != "title":
            self.pause_alarm(self.title_planet_alarm)
        else:
            self.unpause_alarm(self.title_planet_alarm)

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