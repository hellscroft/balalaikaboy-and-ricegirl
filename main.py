import sys
import pygame
from pygame.locals import *
import sqlite3
import time

from src.components.game import Game
from src.components.board import Board
from src.components.character import BalalaikaBoy, RiceGirl
from src.components.controller import ArrowsController, WASDController, GeneralController
from src.components.gate import Gate
from src.components.door import ChineseDoor, RussianDoor
from src.components.level_select import LevelSelect
from src.config import Config
from src.services.music_service import MusicService


def main():
    pygame.init()
    controller = GeneralController()
    game = Game()
    show_intro_screen(game, controller)


def show_intro_screen(game, controller):
    intro_screen = pygame.image.load('data/assets/screens/intro_screen.png')
    game.display.blit(intro_screen, (0, 0))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_level_screen(game, controller):
    level_select = LevelSelect()
    level = game.user_select_level(level_select, controller)
    run_game(game, controller, level)


def show_win_screen(game, controller, completion_time):
    win_screen = pygame.image.load('data/assets/screens/win_screen.png')
    game.display.blit(win_screen, (0, 0))

    font = pygame.font.Font('data/assets/Minecraft.ttf', 48)
    text = font.render(f"YOUR TIME: {completion_time:.2f} SEC", True, (0, 0, 0))
    game.display.blit(text, (260, 330))

    while True:
        game.refresh_window()
        if controller.press_key(pygame.event.get(), K_RETURN):
            show_level_screen(game, controller)


def show_death_screen(game, controller, level):
    death_screen = pygame.image.load('data/assets/screens/death_screen.png')
    game.display.blit(death_screen, (0, 0))
    while True:
        game.refresh_window()
        events = pygame.event.get()
        if controller.press_key(events, K_RETURN):
            run_game(game, controller, level)
        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

def update_best_time(level, new_time):
    conn = sqlite3.connect('data/assets/best_time.db')
    cursor = conn.cursor()

    new_time = float(new_time)  # Ensure new_time is a float

    cursor.execute('SELECT time FROM bt WHERE level = ?', (level,))
    result = cursor.fetchone()

    if result is None or result[0] is None:  # Handle NULL values
        cursor.execute('UPDATE bt SET time = ? WHERE level = ?', (new_time, level))
    else:
        best_time = float(result[0])  # Convert stored time to float
        if new_time < best_time:
            cursor.execute('UPDATE bt SET time = ? WHERE level = ?', (new_time, level))

    conn.commit()
    conn.close()


def run_game(game, controller, level="level1"):
    start_time = time.time()

    if level == "level1":
        board = Board('data/assets/level1.txt')
        gate_location = (585, 287)
        plate_locations = [(485, 338), (685, 338)]
        gate = Gate(gate_location, plate_locations)
        gates = [gate]

        chinese_door_location = (64, 96)
        chinese_door = ChineseDoor(chinese_door_location)
        russian_door_location = (160, 96)
        russian_door = RussianDoor(russian_door_location)
        doors = [chinese_door, russian_door]

        balalaika_boy_location = (64, 672)
        balalaika_boy = BalalaikaBoy(balalaika_boy_location)
        rice_girl_location = (128, 672)
        rice_girl = RiceGirl(rice_girl_location)

    if level == "level2":
        board = Board('data/assets/level2.txt')
        gates = []

        chinese_door_location = (780, 96)
        chinese_door = ChineseDoor(chinese_door_location)
        russian_door_location = (660, 96)
        russian_door = RussianDoor(russian_door_location)
        doors = [chinese_door, russian_door]

        balalaika_boy_location = (32, 672)
        balalaika_boy = BalalaikaBoy(balalaika_boy_location)
        rice_girl_location = (96, 672)
        rice_girl = RiceGirl(rice_girl_location)

    if level == "level3":
        board = Board('data/assets/level3.txt')
        gates = []

        chinese_door_location = (28 * 32, 4 * 32)
        chinese_door = ChineseDoor(chinese_door_location)
        russian_door_location = (5 * 32, 4 * 32)
        russian_door = RussianDoor(russian_door_location)
        doors = [chinese_door, russian_door]

        balalaika_boy_location = (28 * 32, 4 * 32)
        balalaika_boy = BalalaikaBoy(balalaika_boy_location)
        rice_girl_location = (5 * 32, 4 * 32)
        rice_girl = RiceGirl(rice_girl_location)


    arrows_controller = ArrowsController()
    wasd_controller = WASDController()

    clock = pygame.time.Clock()

    while True:
        clock.tick(Config.FPS)
        events = pygame.event.get()
        game.draw_level_background(board)

        game.draw_board(board)
        if gates:
            game.draw_gates(gates)
        game.draw_doors(doors)

        game.draw_player([balalaika_boy, rice_girl])

        arrows_controller.control_player(events, balalaika_boy)
        wasd_controller.control_player(events, rice_girl)

        game.move_player(board, gates, [balalaika_boy, rice_girl])

        game.check_for_death(board, [balalaika_boy, rice_girl])

        game.check_for_gate_press(gates, [balalaika_boy, rice_girl])

        game.check_for_door_open(chinese_door, rice_girl)
        game.check_for_door_open(russian_door, balalaika_boy)

        MusicService.start_background_music()

        game.refresh_window()

        if rice_girl.is_dead() or balalaika_boy.is_dead():
            show_death_screen(game, controller, level)

        if game.level_is_done(doors):
            completion_time = round(time.time() - start_time, 2)
            update_best_time(level, completion_time)

            show_win_screen(game, controller, completion_time)

        if controller.press_key(events, K_ESCAPE):
            show_level_screen(game, controller)

        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()