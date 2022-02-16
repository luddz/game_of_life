import pygame
import time
import numpy as np

white = (255, 255, 255)
black = (0, 0, 0)

# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# @return: true if it should die and false if it should live
def rule_one(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and alive_neighbours < 2 

# Any live cell with two or three live neighbours lives on to the next generation.
def rule_two(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and 3 >= alive_neighbours >= 2

# Any live cell with more than three live neighbours dies, as if by overpopulation.
def rule_three(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and alive_neighbours > 3

# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
def rule_four(alive_neighbours:int, is_alive:bool) -> bool:
    return not is_alive and alive_neighbours == 3

def check_rules(prev_matrix, position) -> bool:
    alive_neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # TODO: out of bounds checks.

            # We should not check our self
            if i == 0 and j == 0:
                continue
            if prev_matrix[(position[0] + i, position[1] + j)] == 1:
                alive_neighbours += 1
    
    is_alive = prev_matrix[(position)] == 1
    return rule_one(alive_neighbours, is_alive) and rule_two(alive_neighbours, is_alive) and rule_three(alive_neighbours, is_alive) and rule_four(alive_neighbours, is_alive)


def run_simulation(display, clock):
    print("Running simmulation")
    simulation_over = False
    x, y = 0, 0
    start_pos_x = 0
    start_pos_y = 0
    start_pos = np.array([(25,25),(26,26)])
    next_matrix = np.zeros((display.get_width(), display.get_height())) # row, column
    prev_matrix = np.zeros((display.get_width(), display.get_height()))
    
    # Setup the start state of the game.
    for pos in start_pos:
        prev_matrix[pos[0]][pos[1]] = 1

    while not simulation_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN  and event.key == pygame.K_q):
                simulation_over = True
        
        x_pos = start_pos_x + x % 800
        y_pos = start_pos_y + y % 600
        # y_pos = start_pos_y + y % 10
        pygame.draw.rect(display, white, [x_pos, y_pos, 10, 10])
        pygame.draw.rect(display, black, [x_pos-1, y_pos-1, 10, 10])

        pygame.display.update()
        clock.tick(75)
        x += 1
        y += 1

    pygame.quit()
    quit()


def setup_simulation():
    pygame.init()
    display_width = 50
    display_height = 50

    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game of life simulation")
    clock = pygame.time.Clock()
    return display, clock


if __name__ == "__main__":
    print("Simulation over...")
    display, clock = setup_simulation()
    run_simulation(display, clock)
    print("Simulation over...")