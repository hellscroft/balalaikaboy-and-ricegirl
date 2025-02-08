import sys
import pygame
from pygame.locals import *
from src.services.music_service import MusicService


class Controller:
    def __init__(self):
        pass

    def control_player(self, events, player):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == self._controls["right"]:
                    player.moving_right = True
                elif event.key == self._controls["left"]:
                    player.moving_left = True
                elif event.key == self._controls["up"]:
                    if player.air_timer < 6:
                        player.jumping = True
                        MusicService.play_jump_sound()

            elif event.type == KEYUP:
                if event.key == self._controls["right"]:
                    player.moving_right = False
                elif event.key == self._controls["left"]:
                    player.moving_left = False
                elif event.key == self._controls["up"]:
                    player.jumping = False

    @staticmethod
    def press_key(events, key):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == key:
                    return True
        return False


class ArrowsController(Controller):
    def __init__(self):
        self._controls = {
            "left": K_LEFT,
            "right": K_RIGHT,
            "up": K_UP
        }
        super().__init__()


class WASDController(Controller):
    def __init__(self):
        self._controls = {
            "left": K_a,
            "right": K_d,
            "up": K_w
        }
        super().__init__()

class GeneralController(Controller):
    pass
