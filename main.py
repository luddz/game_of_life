import pygame
import time
import numpy as np
from rules import *


white = (255, 255, 255)
black = (0, 0, 0)

def run_simulation(display, clock):
    print("Running simmulation")
    simulation_over = False

    start_pos = np.array([(300,300), (300,301), (300,302)])
    # start_pos = np.array([(4, 4), (4, 5), (4, 6)])
    next_matrix = np.zeros((display.get_width(), display.get_height())) # row, column
    prev_matrix = np.zeros((display.get_width(), display.get_height())) # row, column
    
    # Setup the start state of the game.
    for pos in start_pos:
        prev_matrix[pos[0]][pos[1]] = 1

    print(prev_matrix)
    
    while not simulation_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN  and event.key == pygame.K_q):
                simulation_over = True
        
        for row_n, row in enumerate(prev_matrix):
            for column_n, value in enumerate(row):
                ## Draw the values. 
                if value == 1:
                    pygame.draw.rect(display, white, [row_n, column_n, 1, 1])
                else:
                    pygame.draw.rect(display, black, [row_n, column_n, 1, 1])

                next_matrix[row_n][column_n] = 1 if check_rules(prev_matrix, (row_n, column_n)) else 0
        # print(prev_matrix)
        pygame.display.update()
        clock.tick(10)
        prev_matrix = next_matrix

    pygame.quit()
    quit()


def setup_simulation():
    pygame.init()
    display_width = 600
    display_height = 800

    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game of life simulation")
    clock = pygame.time.Clock()
    return display, clock


if __name__ == "__main__":
    print("Starting simulation...")
    display, clock = setup_simulation()
    run_simulation(display, clock)
    print("Simulation over...")