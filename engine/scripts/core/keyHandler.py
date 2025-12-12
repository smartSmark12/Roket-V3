import pygame as pg

class KeyHandler:
    def __init__(self, appInstance):
        self.app = appInstance

        self.keycodes_changed = []

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
            self.keycodes_changed.append(keycode_index)
            #self.app.keys_changed.append(self.app.keys_pressed[keycode_index])

        # this fills out the base data for the keybind dict
        for keyname in self.keybinds:
            self.app.keybinds_pressed[keyname] = False

    def register_keybind(self, keybind_name:str, keycode:int):
        if keybind_name in self.keybinds:
            if keycode not in self.keybinds[keybind_name]:
                self.keybinds[keybind_name].append(keycode)
                self.update_keybind_buffers()
            else:
                print(f"{__name__}: keycode {keycode} already registered with keybind {keybind_name}")

        else:
            self.keybinds[keybind_name] = [keycode]

    def unregister_keybind(self, keybind_name:str, keycode:int):
        if keybind_name in self.keybinds:
            if keycode in self.keybinds[keybind_name]:
                if len(self.keybinds[keybind_name]) == 1:
                    del self.keybinds[keybind_name]
                    self.update_keybind_buffers()
                else:
                    del self.keybinds[keybind_name][keycode]
                    self.update_keybind_buffers()

            else:
                print(f"{__name__}: keycode {keycode} not registered with keybind {keybind_name} - cannot unregister")

        else:
            print(f"{__name__}: keybind {keybind_name} not registered - cannot unregister")

    def update_keybind_buffers(self):
        for keyname in self.keybinds:
            self.app.keybinds_pressed[keyname] = False

    def update_keys(self):
        pressed = pg.key.get_pressed()
        last_pressed = self.app.keys_pressed
        
        for key in range(len(last_pressed)):
            self.keycodes_changed[key] = last_pressed[key] != pressed[key]

        self.app.keys_pressed = pressed

        # update keybinds
        last_pressed_keybinds = self.app.keybinds_pressed.copy()

        for keyname in self.keybinds: # updates currently pressed keybinds
            for keycode in range(len(self.keybinds[keyname])):
                if self.app.keys_pressed[self.keybinds[keyname][keycode]]:
                    self.app.keybinds_pressed[keyname] = True
                    break # sets the keybind pressed to true and continues onto the next keybind

                self.app.keybinds_pressed[keyname] = False
                    
            """ self.app.keybinds_pressed[keyname] = self.app.keys_pressed[self.keybinds[keyname]] """

        for keyname in self.keybinds: # updates all changes in keybind presses
            self.app.keybinds_changed[keyname] = last_pressed_keybinds[keyname] != self.app.keybinds_pressed[keyname]

                #self.app.keybinds_changed[keyname] = self.app.keys_pressed[keycode] != last_pressed_keybinds[keyname]