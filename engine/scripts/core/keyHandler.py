import pygame as pg

class KeyHandler:
    def __init__(self, appInstance):
        self.app = appInstance

    def initial_setup(self):

        self.keybinds = {
            "space":pg.K_SPACE,
            "up":pg.K_UP,
            "right":pg.K_RIGHT,
            "down":pg.K_DOWN,
            "left":pg.K_LEFT,
            "w":pg.K_w,
            "a":pg.K_a,
            "d":pg.K_d,
            "s":pg.K_s
        }

        self.create_key_buffers()

    def create_key_buffers(self):
        self.app.keys_pressed = pg.key.get_pressed()
        self.app.keys_changed = []

        # creates manually assigned keybind dicts ## thank god for KJ playlist on spotify :cry:
        self.app.keybinds_pressed = {}
        self.app.keybinds_changed = {}

        # this is some broken shit
        for keycode_index in range(len(self.app.keys_pressed)):
            self.app.keys_changed.append(self.app.keys_pressed[keycode_index])

        # this fills out the base data for the keybind dict
        for keyname in self.keybinds:
            self.app.keybinds_pressed[keyname] = False

    def update_keys(self):
        pressed = pg.key.get_pressed()
        last_pressed = self.app.keys_pressed
        
        for key in range(len(last_pressed)):
            self.app.keys_changed[key] = last_pressed[key] != pressed[key]

        self.app.keys_pressed = pressed

        # update keybinds
        last_pressed_keybinds = self.app.keybinds_pressed.copy()

        for keyname in self.keybinds: # updates currently pressed keybinds
            self.app.keybinds_pressed[keyname] = self.app.keys_pressed[self.keybinds[keyname]]

        for keyname in self.keybinds: # updates all changes in keybind presses
            keycode = self.keybinds[keyname]
            self.app.keybinds_changed[keyname] = self.app.keys_pressed[keycode] != last_pressed_keybinds[keyname]