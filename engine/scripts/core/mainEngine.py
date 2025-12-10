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

        # load fonts # can hardcode, cause you'll still need to relaunch the game to take effect
        self.h1_font = pg.Font("engine/game/assets/fonts/MinecraftRegular-Bmg3.otf", int(160 * (self.height / HEIGHT)))
        self.button_font = pg.Font("engine/game/assets/fonts/MinecraftRegular-Bmg3.otf", int(80 * (self.height / HEIGHT)))

        # add all scenes
        self.scene_handler.addScene(Scene(self, "main_menu"))
        self.scene_handler.addScene(Scene(self, "ship_modification"))
        self.scene_handler.addScene(Scene(self, "game"))
        self.scene_handler.addScene(Scene(self, "career"))
        self.scene_handler.addScene(Scene(self, "achievements"))
        self.scene_handler.addScene(Scene(self, "settings"))

        # set main scene
        self.scene_handler.setActiveScene("main_menu")

        main_menu_scene = self.scene_handler.getScene("main_menu")
        ship_mod_scene = self.scene_handler.getScene("ship_modification")
        game_scene = self.scene_handler.getScene("game")
        career_scene = self.scene_handler.getScene("career")
        achievements_scene = self.scene_handler.getScene("achievements")
        settings_scene = self.scene_handler.getScene("settings")

        # override scene updates
        main_menu_scene.update = self.main_menu_update

        # override scene renders
        main_menu_scene.render = self.main_menu_render

        # override scene shis

        menu_button_width = 360
        menu_button_height = 160

        menu_square_button_size = 160

        main_menu_scene.main_text = "Roket V3!"
        main_menu_scene.play_text = "PLAY"
        main_menu_scene.exit_text = "EXIT"
        main_menu_scene.buttons = {}
        ## create all menu buttons
        main_menu_scene.buttons["play"] = button(flatpane("sprite", {"main":self.sprites["button_template"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - menu_button_width) / 2), self.to_scale_y((HEIGHT - menu_button_height) / 2), self.to_scale_x(menu_button_width), self.to_scale_y(menu_button_height)), 0, None, partial(print, "play pressed"), None, self)
        main_menu_scene.buttons["exit"] = button(flatpane("sprite", {"main":self.sprites["button_template"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - menu_button_width) / 2), self.to_scale_y((HEIGHT - menu_button_height) / 2 + 200), self.to_scale_x(menu_button_width), self.to_scale_y(menu_button_height)), 0, None, partial(print, "exit pressed"), None, self)
        
        main_menu_scene.buttons["settings"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_settings_button"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - menu_square_button_size) / 2 - 300), self.to_scale_y((HEIGHT - menu_square_button_size) / 2 + 200), self.to_scale_x(menu_square_button_size), self.to_scale_y(menu_square_button_size)), 0, None, partial(print, "options pressed"), None, self)
        main_menu_scene.buttons["achievements"] = button(flatpane("sprite", {"main":self.sprites["mainmenu_leaderboard_button"]}, sprite="main"), pg.Rect(self.to_scale_x((WIDTH - menu_square_button_size) / 2 + 300), self.to_scale_y((HEIGHT - menu_square_button_size) / 2 + 200), self.to_scale_x(menu_square_button_size), self.to_scale_y(menu_square_button_size)), 0, None, partial(print, "achievements pressed"), None, self)

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
            (200, 400)
        ]

    def set_resolution(self):
        self.active_resolution_index = 4
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

    def main_menu_update(self):
        main_menu = self.scene_handler.getScene("main_menu")
        # update all buttons
        for button_index in main_menu.buttons:
            button = main_menu.buttons[button_index]
            button.activation_detection(self.mouse_info)
            button.update_hold_time(self.mouse_info)
            button.render()

    def main_menu_render(self):
        main_menu = self.scene_handler.getScene("main_menu")
        self.draw("text", self.LAYER_UI_TOP, {"text":main_menu.main_text, "no_bg":True, "font":self.h1_font, "center":(self.width/2, self.height/5)})
        self.draw("text", self.LAYER_UI_TOP, {"text":main_menu.play_text, "no_bg":True, "font":self.button_font, "center":main_menu.buttons["play"].rect.center, "color":black})
        self.draw("text", self.LAYER_UI_TOP, {"text":main_menu.exit_text, "no_bg":True, "font":self.button_font, "center":main_menu.buttons["exit"].rect.center, "color":black})


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
        """ if mouse_pressed[0] == self.mouse_last: # could do it for every mouse button and put in in a list as any
            mouse_changed = False
        else:
            mouse_changed = True """

        self.mouse_last = left_pressed

        self.mouse_info = (pg.mouse.get_pos(), left_pressed, mouse_changed)

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
        """ # only renders integrated examples
        self.render_examples()

        self.animations["example_anim"].anim_pos = (self.mouse_info[0][0], self.mouse_info[0][1])

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