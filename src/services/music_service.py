import random

import pygame

from paths import AUDIO_DIR


class MusicService:
    @staticmethod
    def get_background_musics():
        return [
            AUDIO_DIR / "soivet_anthem.mp3",
            AUDIO_DIR / "mao_zedong.mp3",
            AUDIO_DIR / "chinese_rap.mp3",
            AUDIO_DIR / "rasputin_katyusha.mp3"
        ]

    @staticmethod
    def start_background_music():
        if pygame.mixer.music.get_busy():
            return

        musics = MusicService.get_background_musics()
        filename = random.choice(musics)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

    @staticmethod
    def play_jump_sound():
        jump_sfx = pygame.mixer.Sound(AUDIO_DIR / "jump.mp3")
        pygame.mixer.Sound.play(jump_sfx)
