class AnimatedTexture():
    def __init__(self, animation_frames: list, animation_time: int | float, animation_layer:int, animation_position:tuple[int], appInstance):
        self.anim_frames = animation_frames
        self.anim_time = animation_time
        self.anim_layer = animation_layer
        self.anim_pos = animation_position

        self.app = appInstance

        self.active_frame = None
        self.active_frame_index = 0
        self.active_time = 0

        self.frametime = self.get_frame_times()

    def get_frame_times(self):
        try:
            return self.anim_time / len(self.anim_frames)
        except:
            self.app.logger.add_to_log(f"{__name__}: couldn't calculate frametimes (probably no animation frames were given); returning 1")
            return 1
        
    def update_active_frame(self, dt):
        self.active_time += dt #Datablock.floats["dt"]
        while self.active_time > self.frametime:
            self.active_time -= self.frametime
            self.next_frame()

    def next_frame(self):
        self.active_frame_index += 1
        if self.active_frame_index > len(self.anim_frames) - 1:
            self.active_frame_index = 0

    def get_current_frame(self):
        return self.anim_frames[self.active_frame_index]
    
    def get_animation_position(self):
        return self.anim_pos
    
    def get_render_layer(self):
        return self.anim_layer