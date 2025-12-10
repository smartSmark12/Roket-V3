import pygame as pg
import moderngl as mgl

from scripts.core.settings import *
from scripts.renderItem import RenderItem

import _thread
from threading import Lock

class ThreadedGameRenderer:
    def __init__(self, app, thread_lock:Lock):
        self.app = app
        self.lock = thread_lock
        self.window = app.window
        self.layers = self.app.render_layers
        self.window_drawing = self.app.draw_window #pg.Surface(RESOLUTION)

        self.to_render = []

        self.current_log = []

        _thread.start_new_thread(self.render_thread)

    def render_thread(self):

        self.clock = pg.time.Clock()
        self.dt = 0

        while self.app.is_running:
            if SYNC_UPS_FPS:
                self.dt = self.clock.tick(self.app.clock.get_fps()) / 1000
            else:
                self.dt = self.clock.tick(FPS_RENDER_LIMIT) / 1000

            with self.lock:
                self.app.to_render_full.append(RenderItem("text", self.app.LAYER_UI_TOP, {"no_bg":True, "color":(255, 0, 0), "rect":pg.Rect(10, 50, 0, 0), "text":"REN: "+str(round(self.clock.get_fps()))}))
        
            #with self.lock:
                if self.app.to_render_full != None and self.app.to_render_full != []:
                    self.to_render = self.app.to_render_full.copy()

            self.render(self.to_render)

    def render(self, to_render):
        local_to_render = to_render.copy()

        self.window_drawing.fill((0, 0, 0))
        for layer in range(self.layers): # goes through every layer; set number of layers at the top in "engine default variables - layers_current"
            for item in local_to_render: # sprite, rect, line, aaline, circle, text
                if item.layer == layer: # checks if current item is at the set layer, else skips it
                    try:
                        match item.item_type:
                            case "sprite":
                                self.window_drawing.blit(item.metadata["sprite"], item.metadata["rect"])
                            case "rect":
                                pg.draw.rect(self.window_drawing, item.metadata["color"], item.metadata["rect"], item.metadata["width"], item.metadata["radius"])
                            case "line":
                                pg.draw.line(self.window_drawing, item.metadata["color"], item.metadata["start"], item.metadata["end"], item.metadata["width"])
                            case "aaline":
                                pg.draw.aaline(self.window_drawing, item.metadata["color"], item.metadata["start"], item.metadata["end"])
                            case "circle":
                                pg.draw.circle(self.window_drawing, item.metadata["color"], item.metadata["center"], item.metadata["radius"], item.metadata["width"])
                            case "text":
                                if "center" in item.metadata:
                                    item.center_rect = item.metadata["font"].render(item.metadata["text"], False, (0, 0, 0)).get_rect()
                                    item.metadata["rect"] = item.center_rect
                                    item.metadata["rect"].center = item.metadata["center"]
                                if "no_bg" in item.metadata: self.window_drawing.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"]), item.metadata["rect"])
                                else: self.window_drawing.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"]), item.metadata["rect"])
                            case "poly":
                                pg.draw.polygon(self.window_drawing, item.metadata["color"], item.metadata["points"], item.metadata["width"])
                    except:
                        self.current_log.append(f"{__name__}: Item '{item.item_type}' in layer {item.layer} couldn't be rendered; check metadata parameters")

        if OGL_ENABLED:
            with self.lock:
                self.app.window = self.window_drawing.copy() # i probably broke this with the ratio thingie XD

        else:
            self.app.window.blit(self.window_drawing, pg.Rect(self.app.blackbar_x_size_aka_renderer_blit_x_offset, self.app.blackbar_y_size_aka_renderer_blit_y_offset, self.app.width, self.app.height))
            pg.display.flip()

    def render_get_log(self):
        with self.lock:
            send_log = self.current_log.copy()
            self.current_log.clear()
        return send_log

class MainGameRender:
    def __init__(self, app):
        self.app = app
        self.window = app.window
        self.layers = self.app.render_layers
        self.to_render = app.to_render
        self.surf_to_tex = app.ogl_handler.surf_to_tex

        self.render = self.render_old

        self.current_log = []

    def use_renderer(self, useNew:bool=True): # no longer in use
        if useNew: self.render = self.render_new
        else: self.render = self.render_old

    def render_get_log(self):
        send_log = self.current_log.copy()
        self.current_log.clear()
        return send_log
    
    def render_new(self, to_render):
        self.window.fill((0, 0, 0))

        renderitems_sorted = sorted(to_render, key=lambda item: item.layer)

        for item in renderitems_sorted:
            try:
                match item.item_type:
                    case "sprite":
                        self.window.blit(item.metadata["sprite"], item.metadata["rect"])
                    case "rect":
                        pg.draw.rect(self.window, item.metadata["color"], item.metadata["rect"], item.metadata["width"], item.metadata["radius"])
                    case "line":
                        pg.draw.line(self.window, item.metadata["color"], item.metadata["start"], item.metadata["end"], item.metadata["width"])
                    case "aaline":
                        pg.draw.aaline(self.window, item.metadata["color"], item.metadata["start"], item.metadata["end"])
                    case "circle":
                        pg.draw.circle(self.window, item.metadata["color"], item.metadata["center"], item.metadata["radius"], item.metadata["width"])
                    case "text":
                        if "no_bg" in item.metadata: self.window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"]), item.metadata["rect"])
                        else: self.window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"]), item.metadata["rect"])
                    case "poly":
                        pg.draw.polygon(self.window, item.metadata["color"], item.metadata["points"], item.metadata["width"])
            except Exception as e:
                self.current_log.append(f"{__name__}: Item '{item.item_type}' in layer {item.layer} couldn't be rendered; check metadata parameters; (full stack: {e})")

        if OGL_ENABLED:
        
            self.app.ogl_handler.frame_tex = self.surf_to_tex(self.window)
            self.app.ogl_handler.frame_tex.use(0)
            self.app.ogl_handler.program["tex"] = 0
            self.app.ogl_handler.render_object.render(mode=mgl.TRIANGLE_STRIP)
        
        pg.display.flip()

        if OGL_ENABLED:

            self.app.ogl_handler.frame_tex.release()
            

    def render_old(self, to_render):
        self.to_render = to_render
        self.window.fill((0, 0, 0))

        for layer in range(self.layers): # goes through every layer; set number of layers at the top in "engine default variables - layers_current"
            for item in self.to_render: # sprite, rect, line, aaline, circle, text
                if item.layer == layer: # checks if current item is at the set layer, else skips it
                    try:
                        match item.item_type:
                            case "sprite":
                                self.window.blit(item.metadata["sprite"], item.metadata["rect"])
                            case "rect":
                                pg.draw.rect(self.window, item.metadata["color"], item.metadata["rect"], item.metadata["width"], item.metadata["radius"])
                            case "line":
                                pg.draw.line(self.window, item.metadata["color"], item.metadata["start"], item.metadata["end"], item.metadata["width"])
                            case "aaline":
                                pg.draw.aaline(self.window, item.metadata["color"], item.metadata["start"], item.metadata["end"])
                            case "circle":
                                pg.draw.circle(self.window, item.metadata["color"], item.metadata["center"], item.metadata["radius"], item.metadata["width"])
                            case "text":
                                if "no_bg" in item.metadata: self.window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"]), item.metadata["rect"])
                                else: self.window.blit(item.metadata["font"].render(item.metadata["text"], item.metadata["antialias"], item.metadata["color"], item.metadata["bgcolor"]), item.metadata["rect"])
                            case "poly":
                                pg.draw.polygon(self.window, item.metadata["color"], item.metadata["points"], item.metadata["width"])
                    except:
                        self.current_log.append(f"{__name__}: Item '{item.item_type}' in layer {item.layer} couldn't be rendered; check metadata parameters")

        if OGL_ENABLED:
        
            self.app.ogl_handler.frame_tex = self.surf_to_tex(self.window)
            self.app.ogl_handler.frame_tex.use(0)
            self.app.ogl_handler.program["tex"] = 0
            self.app.ogl_handler.render_object.render(mode=mgl.TRIANGLE_STRIP)
        
        else:
            self.window = self.window #????
        
        pg.display.flip()

        if OGL_ENABLED:

            self.app.ogl_handler.frame_tex.release()