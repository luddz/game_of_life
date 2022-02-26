from json.tool import main
from operator import ne
from tkinter import mainloop
import numpy as np


# Any live cell with fewer than two live neighbours dies, as if by underpopulation.
# @return: true if it should live and false if it should die
def rule_one(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and alive_neighbours >= 2

# Any live cell with two or three live neighbours lives on to the next generation.
def rule_two(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and 3 >= alive_neighbours >= 2

# Any live cell with more than three live neighbours dies, as if by overpopulation.
def rule_three(alive_neighbours:int, is_alive:bool) -> bool:
    return is_alive and alive_neighbours <= 3

# Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
def rule_four(alive_neighbours:int, is_alive:bool) -> bool:
    return not is_alive and alive_neighbours == 3

def check_rules(prev_matrix, position) -> bool:
    alive_neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            
            test_x = position[0] + i
            test_y = position[1] + j
            # Check so we are not checking our own position
            # Out of bounds checks.
            if (test_x, test_y) == position  or test_x < 0 or test_x >= prev_matrix.shape[0] or test_y < 0 or test_y >= prev_matrix.shape[1]:
                continue
    
            if prev_matrix[(test_x, test_y)] == 1:
                alive_neighbours += 1

    is_alive = prev_matrix[(position)] == 1
    # print(f"\nResult rule_one: {rule_one(alive_neighbours, is_alive)}")
    # print(f"Result rule_two: {rule_two(alive_neighbours, is_alive)}")
    # print(f"Result rule_three: {rule_three(alive_neighbours, is_alive)}")
    # print(f"Result rule_four: {rule_four(alive_neighbours, is_alive)} \n")
    return rule_one(alive_neighbours, is_alive) or rule_two(alive_neighbours, is_alive) or rule_three(alive_neighbours, is_alive) or rule_four(alive_neighbours, is_alive)


class RulesTesting:

    def run_one_step(self, prev_board) -> np.array:
        next_board = np.zeros_like(prev_board)
        for row_n, row in enumerate(prev_board):
            for column_n, _ in enumerate(row):
                next_board[row_n][column_n] = 1 if check_rules(prev_board, (row_n, column_n)) else 0

        return next_board

    def test_single_point(self) -> bool:
        start_board = np.zeros((self.width, self.height))
        start_pos = (5,5)
        start_board[start_pos] = 1
        next_board = self.run_one_step(start_board)
        return np.equal(self.zero_board, next_board).all()

    def test_empty_board(self) -> bool:
        start_board = np.zeros((self.width, self.height))
        next_board = self.run_one_step(start_board)
        return np.equal(self.zero_board, next_board).all()

    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.prev_board = np.zeros((self.width, self.height))
        self.zero_board = np.zeros_like(self.prev_board)
        self.next_board = np.zeros_like(self.prev_board)


if __name__ == '__main__':
    test = RulesTesting()
    test_results = []
    test_results.append(test.test_empty_board())
    test_results.append(test.test_single_point())

    for n, res in enumerate(test_results):
        p = "Passed"
        f = "failed"
        print(f"Test {n} was {p if res else f}")
