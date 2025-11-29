class GameObject():
    def __init__(self, layer, position, object_type, texture_type, metadata, on_click_event, on_hover_event, on_load_event):
        self.layer = layer # layer for this object to be rendered in (for scene, UI, Menus and stuff)
        self.position = position # position of object (for Menu, object in scene...)
        self.object_type = object_type # rigidbody, kinematicbody, particle spawner, uielement, entity?
        self.metadata = metadata # big dictionary for additional info
        self.texture_type = texture_type # idk why this's here
        self.on_click = on_click_event # happens, when you click on the collider of this object
        self.on_hover = on_hover_event # same, but with hover
        self.on_load = on_load_event # happens, when the object loads for the first time (for later, when you'd be able to initialize the object without actually spawning it in game)

        if self.object_type == "rigid":
            pass # vytvoření rigidbody s parametry (asi self."params"?)

    def move(self, offset):
        self.position += offset

    def move_to(self, position):
        self.position_read = position
        self.destination = (self.position_read[0] * math.cos(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])), self.position_read[1] * math.sin(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])))
        self.angle = math.atan2(self.destination[1] - self.position[1], self.destination[0] - self.position[0]) # tohle chce ještě pořádně prohlédnout

    def move_towards(self, object):
        self.object = object
        self.destination = (self.position_read[0] * math.cos(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])), self.position_read[1] * math.sin(math.atan2(self.position_read[1] - self.position[1], self.position_read[0] - self.position[0])))
        self.angle = math.atan2(self.destination[1] - self.position[1], self.destination[0] - self.position[0]) # tohle chce ještě pořádně prohlédnout

    def exponential_move(self):
        pass

    def move_in_out(self):
        pass

    """ def on_click(self) """

    def destroy(self):
        pass

    def render(self):
        if self.texture_type == "sprite":
            render_object = MainEngine.RenderItem("sprite", 1, {})
        try:
            app.to_render.append(render_object)
        except: pass