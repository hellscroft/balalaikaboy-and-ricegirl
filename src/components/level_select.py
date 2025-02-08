import pygame
from pygame.locals import *


class LevelSelect():
    def __init__(self):
        self.load_images()

    def load_images(self):
        self.screen = pygame.image.load('data/assets/screens/level_select_screen.png')
        self.titles = {
            1: pygame.image.load('data/assets/screens/level1.png'),
            2: pygame.image.load('data/assets/screens/level2.png'),
            3: pygame.image.load('data/assets/screens/level3.png'),
        }

        self.indicator_image = pygame.image.load('data/assets/screens/indicator.png')

        big_player_size = (128, 256)
        self.left_player = pygame.image.load('data/assets/player_images/ricegirl.png')
        self.left_player = pygame.transform.scale(
            self.left_player, big_player_size)
        self.right_player = pygame.image.load('data/assets/player_images/balalaikaboy.png')
        self.right_player = pygame.transform.scale(
            self.right_player, big_player_size)
