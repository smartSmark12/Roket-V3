# modified; will backport to Nebula cause the original implementation is shit
class AnimatedTexture():
    def __init__(self, animation_frames: list, animation_time: int | float):
        if len(animation_frames) == 0:
            print(f"{__name__}: fatal error! no animation frames were provided")

        self.anim_frames = animation_frames
        self.anim_time = animation_time

        self.sprite = self.anim_frames[0]
        self._active_frame_index = 0
        self._active_time = 0

        self._frametime = self._get_frame_times()

    def _get_frame_times(self) -> float:
        try:
            return self.anim_time / len(self.anim_frames)
        except:
            print(f"{__name__}: couldn't calculate frametimes (probably no animation frames were given); returning 1")
            return 1.0
        
    def update_active_frame(self, dt):
        self._active_time += dt
        while self._active_time > self._frametime:
            self._active_time -= self._frametime
            self.next_frame()

            self.sprite = self.anim_frames[self._active_frame_index]

    def next_frame(self):
        self._active_frame_index += 1
        if self._active_frame_index > len(self.anim_frames) - 1:
            self._active_frame_index = 0

    def get_current_frame(self):
        return self.anim_frames[self._active_frame_index]