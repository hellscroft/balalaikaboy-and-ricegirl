import pygame
from pygame.locals import *
from src.config import Config
import math
import sqlite3


class Game:
    def __init__(self):
        WINDOW_SIZE = (Config.WIDTH, Config.HEIGHT)
        self.screen = pygame.display.set_mode(WINDOW_SIZE, pygame.RESIZABLE)
        pygame.display.set_caption("BalalaikaBoy and RiceGirl")
        self.best_times = self.get_best_times()


        CHUNK_SIZE = 32
        DISPLAY_SIZE = (34 * CHUNK_SIZE, 25 * CHUNK_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE)

    def draw_level_screen(self, level_select):
        self.display.blit(level_select.screen, (0, 0))

        for level in range(3):
            image = level_select.titles[level + 1]
            title_x = (self.display.get_width() - image.get_width()) / 2
            title_y = 80 * level + 300
            self.display.blit(image, (title_x, title_y))

        left_cords = (190, 450)
        right_cords = (785, 450)
        self.display.blit(level_select.left_player, left_cords)
        self.display.blit(level_select.right_player, right_cords)
        font = pygame.font.Font('data/assets/Minecraft.ttf', 32)

        lines = [
            f"BEST TIME: "
            f"LEVEL 1: {self.best_times['level1'] if self.best_times['level1'] else 'N/A'},",
            f"LEVEL 2: {self.best_times['level2'] if self.best_times['level2'] else 'N/A'},   "
            f"LEVEL 3: {self.best_times['level3'] if self.best_times['level3'] else 'N/A'}"
        ]

        y_offset = 150
        x_offset = 320

        for line in lines:
            text = font.render(line, True, (255, 255, 255))
            self.display.blit(text, (x_offset, y_offset))
            y_offset += 60
            x_offset -= 50
    def user_select_level(self, level_select, controller):
        level_index = 0
        level_dict = {
            0: "level1",
            1: "level2",
            2: "level3",
        }
        while True:
            self.draw_level_screen(level_select)
            events = pygame.event.get()
            if controller.press_key(events, K_DOWN):
                level_index += 1
                if level_index == 3:
                    level_index = 0
            if controller.press_key(events, K_UP):
                level_index -= 1
                if level_index == -1:
                    level_index = 2
            self.draw_level_select_indicator(level_select, level_index)

            if controller.press_key(events, K_RETURN):
                return level_dict[level_index]

    def draw_level_select_indicator(self, level_select, level_index):
        indicator = level_select.indicator_image
        location_x = (self.display.get_width() - indicator.get_width()) / 2
        location_y = level_index * 80 + 292
        indicator_location = (location_x, location_y)
        self.display.blit(level_select.indicator_image, indicator_location)
        self.refresh_window()

    def refresh_window(self):
        new_window_size, center_cords = self.adjust_scale()
        new_disp = pygame.transform.scale(self.display, new_window_size)
        self.screen.blit(new_disp, center_cords)
        pygame.display.update()

    def adjust_scale(self):
        window_size = self.screen.get_size()

        if window_size[0] / window_size[1] >= 1.5:
            display_size = (int(1.5 * window_size[1]), window_size[1])
        else:
            display_size = (window_size[0], int(.75 * window_size[0]))
        cords = ((window_size[0] - display_size[0]) / 2,
                 (window_size[1] - display_size[1]) / 2)

        return display_size, cords


    def draw_level_background(self, board):
        self.display.blit(board.get_background(), (0, 0))

    def draw_board(self, board):
        board_textures = board.get_board_textures()
        for y, row in enumerate(board.get_game_map()):
            for x, tile in enumerate(row):
                if tile != "0":
                    self.display.blit(
                        board_textures[f"{tile}"], (x * 32, y * 32)
                    )

    def draw_gates(self, gates):
        for gate in gates:
            self.display.blit(gate.gate_image, gate.gate_location)

            for location in gate.plate_locations:
                self.display.blit(gate.plate_image, location)

    def draw_doors(self, doors):
        for door in doors:
            self.display.blit(door.door_background, door.background_location)
            self.display.blit(door.door_image, door.door_location)
            self.display.blit(door.frame_image, door.frame_location)

    def draw_player(self, players):
        for player in players:
            if player.moving_right:
                player.animate()
                player.update()
                player_image = player.side_image
            elif player.moving_left:
                player.animate()
                player.update()
                player_image = pygame.transform.flip(
                    player.side_image, True, False)
            else:
                player_image = player.image
            self.display.blit(player_image, (player.rect.x, player.rect.y))

    def move_player(self, board, gates, players):
        for player in players:
            player.calc_movement()
            movement = player.get_movement()

            collide_blocks = board.get_solid_blocks()
            for gate in gates:
                collide_blocks += gate.get_solid_blocks()

            collision_types = {
                'top': False,
                'bottom': False,
                'right': False,
                'left': False}

            player.rect.x += movement[0]
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[0] > 0:
                    player.rect.right = tile.left
                    collision_types['right'] = True
                elif movement[0] < 0:
                    player.rect.left = tile.right
                    collision_types['left'] = True

            player.rect.y += movement[1]
            hit_list = self.collision_test(player.rect, collide_blocks)
            for tile in hit_list:
                if movement[1] > 0:
                    player.rect.bottom = tile.top
                    collision_types['bottom'] = True
                elif movement[1] < 0:
                    player.rect.top = tile.bottom
                    collision_types['top'] = True

            if collision_types['bottom']:
                player.y_velocity = 0
                player.air_timer = 0
            else:
                player.air_timer += 1

            if collision_types['top']:
                player.y_velocity = 0

    def check_for_death(self, board, players):
        for player in players:
            if player.get_type() == "russian":
                is_killed = self.collision_test(
                    player.rect, board.get_lava_pools())
            if player.get_type() == "chinese":
                is_killed = self.collision_test(
                    player.rect, board.get_water_pools())
            is_killed += self.collision_test(player.rect, board.get_slime_pools())

            if is_killed:
                player.kill_player()

    def check_for_gate_press(self, gates, players):
        for gate in gates:
            plate_collisions = []
            for player in players:
                plates = gate.get_plates()
                plate_collisions += self.collision_test(player.rect, plates)
            if plate_collisions:
                gate.plate_is_pressed = True
            else:
                gate.plate_is_pressed = False
            gate.try_open_gate()

    def check_for_door_open(self, door, player):
        door_collision = self.collision_test(player.rect, [door.get_door()])
        if door_collision:
            door.player_at_door = True
        else:
            door.player_at_door = False
        door.try_raise_door()

    @staticmethod
    def level_is_done(doors):
        is_win = True
        for door in doors:
            if not door.is_door_open():
                is_win = False
        return is_win

    @staticmethod
    def collision_test(rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    @staticmethod
    def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
        t = pygame.time.get_ticks() / 2 % time
        y = math.sin(t / speed) * how_far + overall_y
        return int(y)

    @staticmethod
    def get_best_times():
        conn = sqlite3.connect('data/assets/best_time.db')
        cursor = conn.cursor()

        best_times = {}
        for level in ['level1', 'level2', 'level3']:
            cursor.execute('SELECT time FROM bt WHERE level = ?', (level,))
            result = cursor.fetchone()
            best_times[level] = result[0] if result else None

        conn.close()
        return best_times