import pygame
from pygame.locals import *
from src.config import Config


class Character:
    def __init__(self, location):
        _location = location
        self.rect = pygame.Rect(
            location[0], location[1], self.image.get_width(),
            self.image.get_height())
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.y_velocity = 0
        self.air_timer = 0
        self._alive = True

    def calc_movement(self):

        self._movement = [0, 0]
        if self.moving_right:
            self._movement[0] += Config.LATERAL_SPEED
        if self.moving_left:
            self._movement[0] -= Config.LATERAL_SPEED

        if self.jumping:
            self.y_velocity = Config.JUMP_SPEED
            self.jumping = False
        self._movement[1] += self.y_velocity
        self.y_velocity += Config.GRAVITY
        if self.y_velocity > Config.TERMINAL_VELOCITY:
            self.y_velocity = Config.TERMINAL_VELOCITY

    def kill_player(self):
        self._alive = False

    def get_movement(self):
        return self._movement

    def is_dead(self):
        return self._alive is False

    def get_type(self):
        return self._type


class BalalaikaBoy(Character):
    def __init__(self, location):
        self.image = pygame.image.load('data/assets/player_images/balalaikaboy.png')
        self.sprites = [pygame.image.load('data/assets/player_images/balalaikaboyside1.png'),
                        pygame.image.load('data/assets/player_images/balalaikaboyside2.png'),
                        pygame.image.load('data/assets/player_images/balalaikaboyside3.png'),
                        pygame.image.load('data/assets/player_images/balalaikaboyside4.png')]
        self.current_sprite = 0
        self.side_image = self.sprites[self.current_sprite]

        self.rect = self.side_image.get_rect()
        self.rect.topleft = location
        self._type = "russian"
        super().__init__(location)

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.side_image = self.sprites[int(self.current_sprite)]


class RiceGirl(Character):
    def __init__(self, location):
        self.image = pygame.image.load('data/assets/player_images/ricegirl.png')
        self.sprites = [pygame.image.load('data/assets/player_images/ricegirlside1.png'),
                        pygame.image.load('data/assets/player_images/ricegirlside2.png'),
                        pygame.image.load('data/assets/player_images/ricegirlside3.png'),
                        pygame.image.load('data/assets/player_images/ricegirlside4.png')]
        self.current_sprite = 0
        self.side_image = self.sprites[self.current_sprite]

        self.rect = self.side_image.get_rect()
        self.rect.topleft = location
        self._type = "chinese"
        super().__init__(location)

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0

            self.side_image = self.sprites[int(self.current_sprite)]
