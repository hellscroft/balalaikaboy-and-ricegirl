import pygame


class Board:
    def __init__(self, path):
        self.path = path
        self.CHUNK_SIZE = 32
        self.load_map(path)
        self.load_images()
        self.make_solid_blocks()
        self.make_water_pools()
        self.make_lava_pools()
        self.make_slime_pools()

    def load_map(self, path):
        self._game_map = []

        with open(path) as f:
            for line in f:
                line = line.strip().split(',')
                self._game_map.append(line)

    def get_game_map(self):
        return self._game_map

    def load_images(self):
        if self.path == 'data/assets/level1.txt':
            self._background = pygame.image.load('data/assets/board_textures/wall.png')
        elif self.path == 'data/assets/level2.txt':
            self._background = pygame.image.load('data/assets/board_textures/wall2.png')
        elif self.path == 'data/assets/level3.txt':
              self._background = pygame.image.load('data/assets/board_textures/wall3.png')

        self._board_textures = {
            "100": pygame.image.load('data/assets/board_textures/100.png'),
            "100": pygame.image.load('data/assets/board_textures/100.png'),
            "111": pygame.image.load('data/assets/board_textures/111.png'),
            "112": pygame.image.load('data/assets/board_textures/112.png'),
            "113": pygame.image.load('data/assets/board_textures/113.png'),
            "114": pygame.image.load('data/assets/board_textures/114.png'),
            "121": pygame.image.load('data/assets/board_textures/121.png'),
            "122": pygame.image.load('data/assets/board_textures/122.png'),
            "123": pygame.image.load('data/assets/board_textures/123.png'),
            "124": pygame.image.load('data/assets/board_textures/124.png'),
            "2": pygame.image.load('data/assets/board_textures/lava.png'),
            "3": pygame.image.load('data/assets/board_textures/water.png'),
            "4": pygame.image.load('data/assets/board_textures/slime.png')
        }

    def get_background(self):
        return self._background

    def get_board_textures(self):
        return self._board_textures

    def make_solid_blocks(self):
        self._solid_blocks = []
        for y, row in enumerate(self._game_map):
            for x, tile in enumerate(row):
                if tile not in ['0', '2', '3', '4']:
                    self._solid_blocks.append(
                        pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE,
                                    self.CHUNK_SIZE, self.CHUNK_SIZE))

    def get_solid_blocks(self):
        return self._solid_blocks

    def make_lava_pools(self):
        self._lava_pools = []
        for y, row in enumerate(self._game_map):
            for x, tile in enumerate(row):
                if tile == "2":
                    self._lava_pools.append(
                        pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE
                                    + self.CHUNK_SIZE / 2, self.CHUNK_SIZE,
                                    self.CHUNK_SIZE / 2))

    def get_lava_pools(self):
        return self._lava_pools

    def make_water_pools(self):
        self._water_pools = []
        for y, row in enumerate(self._game_map):
            for x, tile in enumerate(row):
                if tile == "3":
                    self._water_pools.append(
                        pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE
                                    + self.CHUNK_SIZE / 2, self.CHUNK_SIZE,
                                    self.CHUNK_SIZE / 2))

    def get_water_pools(self):
        return self._water_pools

    def make_slime_pools(self):
        self._slime_pools = []
        for y, row in enumerate(self._game_map):
            for x, tile in enumerate(row):
                if tile == "4":
                    self._slime_pools.append(
                        pygame.Rect(x * self.CHUNK_SIZE, y * self.CHUNK_SIZE
                                    + self.CHUNK_SIZE / 2, self.CHUNK_SIZE,
                                    self.CHUNK_SIZE / 2))

    def get_slime_pools(self):
        return self._slime_pools
