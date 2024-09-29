# This code sets up the Robot Escape Game for use in CPSC231
# By Richard Zhao
# This file should not be edited in any way for the assignment
# Your code should be created in a new, separate file called board.py

import pygame
from pygame.locals import *
import sys
import board

BLACK = (30, 30, 30)
WHITE = (250, 250, 250)
BLUE = (0, 0, 255)
GREEN = (0, 100, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 800
ROW = 12
COL = 16


def draw_grid(game_grid, game_over, steps):
    block_size = 50  # Set the size of the grid block

    if game_grid == []:
        game_grid = [[" " for j in range(COL)] for i in range(ROW)]

    if len(game_grid) != ROW or len(game_grid[0]) != COL:
        print("Wrong size for grid. Grid must have 12 rows and 16 columns.")
    else:

        for x in range(len(game_grid)):
            if len(game_grid[x]) == COL:
                for y in range(COL):
                    rect = pygame.Rect(y * block_size, x * block_size, block_size, block_size)
                    if game_grid[x][y] == "#":
                        pygame.draw.rect(SCREEN, BLACK, rect, 0)
                    elif game_grid[x][y] == "P":
                        pygame.draw.circle(SCREEN, GREY,
                                           (y * block_size + block_size // 2, x * block_size + block_size // 2),
                                           block_size // 2)
                    elif game_grid[x][y] == "E":
                        pygame.draw.rect(SCREEN, BLUE, rect, 15)

                    pygame.draw.rect(SCREEN, GREY, rect, 1)

        steps_text = font.render('Step: ' + str(steps), True, WHITE, BLACK)
        SCREEN.blit(steps_text, (5, 5))

        if game_over == 1:
            end_text = font.render('You win!', True, WHITE, GREEN)
            SCREEN.blit(end_text, (330, 250))
        elif game_over == 2:
            end_text = font.render('You lost.', True, WHITE, BLACK)
            SCREEN.blit(end_text, (350, 250))
        elif game_over == 3:
            end_text = font.render('You could do better!', True, WHITE, GREEN)
            SCREEN.blit(end_text, (290, 250))


# start of the Robot Escape Game
if __name__ == "__main__":
    # create the current board object
    current_board = board.Board()

    # Initialize pygame
    pygame.init()

    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(BLACK)
    pygame.display.set_caption("Robot Escape Game - CPSC 231 Fall 2023 University of Calgary")
    font_color = (0, 150, 250)
    font = pygame.font.SysFont("Segoe UI", 30)

    print("\nUse WASD or the arrow keys to move. Press Esc to quit the game.\n")
    done = False
    game_over = 0
    steps = 0

    while not done:
        SCREEN.fill((255, 255, 255))
        draw_grid(current_board.get_board(), game_over, steps)

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            # when a key is pressed and the game is not over
            elif event.type == KEYDOWN and not game_over:
                # right key or D
                if event.key == K_RIGHT or event.key == K_d:
                    current_board.update("R")
                    steps += 1
                # left key or A
                elif event.key == K_LEFT or event.key == K_a:
                    current_board.update("L")
                    steps += 1
                # up key or W
                elif event.key == K_UP or event.key == K_w:
                    current_board.update("U")
                    steps += 1
                # down key or S
                elif event.key == K_DOWN or event.key == K_s:
                    current_board.update("D")
                    steps += 1
                # L key for loading a game
                elif event.key == K_l:
                    current_board.load_game()
                    steps = current_board.get_steps()
                    draw_grid(current_board.get_board(), game_over, steps)
                # J key for saving a game
                elif event.key == K_j:
                    current_board.save_game()

                game_over = current_board.get_state()

        keys = pygame.key.get_pressed()
        # Escape exits the game
        if keys[K_ESCAPE]:
            done = True

        pygame.display.update()

    pygame.display.quit()
    pygame.quit()
    sys.exit()
