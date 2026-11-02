import pygame as pg

from scripts.json_loader import JsonLoader

class SoundManager:
    def __init__(self, appInstance):
        pg.mixer.init()
        self.app = appInstance

        self.sounds:dict[str, pg.mixer.Sound] = {}
        self.music = {}

        self.active_music = None

    # SOUNDS
    def load_sound(self, soundName:str, soundPath:str) -> pg.mixer.Sound:
        try:
            sound = pg.mixer.Sound(soundPath)
            self.sounds[soundName] = sound
            return sound
        
        except:
            print(f"{__name__}: couldn't load sound '{soundName}'")

    def unload_sound(self, soundName:str):
        if soundName in self.sounds:
            self.sounds.pop(soundName)

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to unload (did you forget to load it first?)")

    def get_sound(self, soundName:str):
        if soundName in self.sounds:
            return self.sounds.get(soundName)

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' (did you forget to load it first?)")
        return None

    def set_sound_volume(self, soundName:str, volume:float=1.0):
        if soundName in self.sounds:
            if volume <= 1.0 and volume >= 0.0:
                self.sounds.get(soundName).set_volume(value=volume)
            else:
                print(f"{__name__}: can only accept volumes between 0-1, volume {volume} not accepted")

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to set volume of (did you forget to load it first?)")

    def get_sound_volume(self, soundName:str):
        if soundName in self.sounds:
            return self.sounds.get(soundName).get_volume()

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to get volume of (did you forget to load it first?)")
            return 1.0

    def get_sound_active_channels(self, soundName:str):
        if soundName in self.sounds:
            return self.sounds.get(soundName).get_num_channels()

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to get active channels of (did you forget to load it first?)")
            return 0

    def get_sound_length_sec(self, soundName:str):
        if soundName in self.sounds:
            return self.sounds.get(soundName).get_length()

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to get length of (did you forget to load it first?)")
            return 1.0

    def play_sound(self, soundName:str, fadeInMS:int):
        if soundName in self.sounds:
            self.sounds.get(soundName).play(fade_ms=fadeInMS)

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to play (did you forget to load it first?)")

    def stop_sound(self, soundName:str):
        if soundName in self.sounds:
            self.sounds.get(soundName).stop()

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to stop (did you already unload it?)")

    def fadeout_stop_sound(self, soundName:str, fadeOutMS:int):
        if soundName in self.sounds:
            self.sounds.get(soundName).fadeout(time=fadeOutMS)

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to stop (did you already unload it?)")

    def get_sound_is_playing(self, soundName:str):
        if soundName in self.sounds:
            return self.sounds.get(soundName).get_num_channels() > 0

        else:
            print(f"{__name__}: couldn't find sound '{soundName}' to check if its playing (did you forget to load it first?)")
            return 0

    def get_any_sound_is_playing(self):
        return pg.mixer.get_busy()

    def set_number_of_channels(self, amount:int=8):
        try:
            pg.mixer.set_num_channels(count=amount)
        except Exception as e:
            print(f"{__name__}: couldn't set the number of channels to {amount}, \n{e}")

    def get_number_of_channels(self):
        return pg.mixer.get_num_channels()

    def load_sounds_from_file(self, filePath:str):
        sounds_file = JsonLoader.load_from_file(filepath=filePath)

        for sound in sounds_file:
            self.load_music(sound, sounds_file.get(sound))


    # MUSIC
    def load_music(self, musicName:str, musicPath:str):
        try:
            self.music[musicName] = musicPath

        except:
            print(f"{__name__}: couldn't load music '{musicName}'")

    def get_music_path(self, musicName:str) -> str|None:
        if musicName in self.music:
            return self.music.get(musicName)

        else:
            print(f"{__name__}: couldn't find music '{musicName}' (did you forget to load it first?)")
            return None

    def set_music_volume(self, volume:float=1.0):
        if volume <= 1.0 and volume >= 0.0:
            pg.mixer.music.set_volume(volume=volume)
        else:
            print(f"{__name__}: can only accept volumes between 0-1, volume {volume} not accepted")

    def get_music_volume(self):
        return pg.mixer.music.get_volume()

    def play_music(self, musicName:str, repeat:bool=False, offset:float=0, fadeInMS:int=0):
        if musicName in self.music.keys():
            try:
                pg.mixer.music.load(self.music.get(musicName))
            except:
                print(f"{__name__}: couldn't fetch music file to play (does the file exist and does it follow the right format? [pure OGG Vorbis; no thumbnail etc.])")
            try:
                pg.mixer.music.play(loops=-1 if repeat else 0, start=offset, fade_ms=fadeInMS)

                self.active_music = musicName

            except Exception as e:
                print(f"{__name__}: couldn't play music '{musicName}': \n{e}")

        else:
            print(f"{__name__}: couldn't find music '{musicName}' to play (did you forget to load it first?)")

    def set_music_play_pos(self, playPositionSec:float):
        try:
            pg.mixer.music.set_pos(playPositionSec)
        except Exception as e:
            print(f"{__name__}: couldn't set music play position of {playPositionSec} seconds, \n{e}")

    def get_music_play_time_ms(self):
        return pg.mixer.music.get_pos()

    def stop_music(self):
        pg.mixer.music.stop()

    def fadeout_stop_music(self, fadeOutMS:int):
        pg.mixer.music.fadeout(time=fadeOutMS)

    def pause_music(self):
        pg.mixer.music.pause()

    def unpause_music(self):
        pg.mixer.music.unpause()

    def get_music_is_playing(self):
        return pg.mixer.music.get_busy()

    def get_active_or_last_music_name(self):
        return self.active_music

    def list_all_loaded_music(self) -> None:
        print(f"{__name__}: all loaded music:\n")
        for musicName, musicPath in self.music.items():
            print(f"{musicName} -> {musicPath}")

    def load_music_from_file(self, filePath:str):
        music_file = JsonLoader.load_from_file(filepath=filePath)

        for music in music_file:
            self.load_music(music, music_file.get(music))



