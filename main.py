import pygame
import time


white = (255, 255, 255)
black = (0, 0, 0)

# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
def rule_one():
    return

# Any live cell with two or three live neighbours lives on to the next generation.
def rule_two():
    return

# Any live cell with more than three live neighbours dies, as if by overpopulation.
def rule_three():
    return

# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
def rule_four():
    return

def run_simulation(display, clock):
    print("Running simmulation")
    simulation_over = False
    x, y = 0, 0
    start_pos_x = 0
    start_pos_y = 0
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
    display_width = 800
    display_height = 600

    display = pygame.display.set_mode((display_width, display_height))

    pygame.display.set_caption("Game of life simulation")
    clock = pygame.time.Clock()
    return display, clock




if __name__ == "__main__":
    print("Simulation over...")
    display, clock = setup_simulation()
    run_simulation(display, clock)
    print("Simulation over...")