import pygame
import numpy as np
from gameOfLife import *


white = (255, 255, 255)
black = (0, 0, 0)

def run_simulation(display, clock):
    print("Running simmulation")
    simulation_over = False

    start_pos = [ (300,300), (300,301), (300,302) ]
    gol = GameOfLife(display.get_width(), display.get_height())
    gol.set_start_pos(start_pos)

    while not simulation_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN  and event.key == pygame.K_q):
                simulation_over = True
        
        for row_n, row in enumerate(gol.state):
            for column_n, value in enumerate(row):
                ## Draw the values. 
                if value == 1:
                    pygame.draw.rect(display, white, [row_n, column_n, 1, 1])
                else:
                    pygame.draw.rect(display, black, [row_n, column_n, 1, 1])

        pygame.display.update()
        clock.tick(10)
        gol.run_one_step()

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