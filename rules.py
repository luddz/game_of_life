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

def check_alive_cell(alive_neighbours:int, is_alive:bool) -> bool:
    return rule_one(alive_neighbours, is_alive) and rule_two(alive_neighbours, is_alive) and rule_three(alive_neighbours, is_alive)

def check_rules(prev_matrix, position) -> bool:
    alive_neighbours = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            test_x = position[0] + i
            test_y = position[1] + j
            # Check so we are not checking our own position and OB checks.
            if (test_x, test_y) == position  or test_x < 0 or test_x >= prev_matrix.shape[0] or test_y < 0 or test_y >= prev_matrix.shape[1]:
                continue
    
            if prev_matrix[(test_x, test_y)] == 1:
                alive_neighbours += 1

    is_alive = prev_matrix[(position)] == 1 
    return check_alive_cell(alive_neighbours, is_alive) if is_alive else rule_four(alive_neighbours, is_alive)


class RulesTesting:

    def run_one_step(self, prev_board) -> np.array:
        next_board = np.zeros_like(prev_board)
        for row_n, row in enumerate(prev_board):
            for column_n, _ in enumerate(row):
                next_board[row_n][column_n] = 1 if check_rules(prev_board, (row_n, column_n)) else 0

        return next_board

    def run_all_tests(self) -> None:
        tests = []
        tests.append(("Empty", self.test_empty_board()))
        tests.append(("Single point", self.test_single_point()))
        tests.append(("Two points seperated", self.test_two_points_seperated()))
        tests.append(("Two points together", self.test_two_points_together()))
        tests.append(("Block", self.test_block()))
        tests.append(("Bee hive", self.test_bee_hive()))
        tests.append(("Loaf", self.test_loaf()))
        tests.append(("Boat", self.test_boat()))
        tests.append(("Tub", self.test_tub()))
        tests.append(("Blinker", self.test_blinker()))
        tests.append(("Beacon", self.test_beacon()))

        for name, res in tests:
            p, f  = "Passed", "Failed"
            print(f"{p if res else f} test {name}")

    def test_static_from_start_pos(self, start_poses):
        start_board = np.copy(self.zero_board)
        for pos in start_poses:
            start_board[pos] = 1
        return np.array_equal(start_board ,  self.run_one_step(start_board))
    
    def test_transformation_from_start_to_final(self, start_poses, final_poses):
        start_board, final_board = np.copy(self.zero_board), np.copy(self.zero_board)
        for pos in start_poses:
            start_board[pos] = 1
        
        for pos in final_poses:
            final_board[pos] = 1
        
        return np.array_equal(final_board , self.run_one_step(start_board))

    def test_block(self) -> bool:
        start_poses = [(5,5), (6,5), (5,6), (6,6)]
        return self.test_static_from_start_pos(start_poses=start_poses)

    def test_bee_hive(self) -> bool:
        # start_poses = [(5,5), (6,5), (4,6), (7,6), (5,7), (6,7)] #Column major
        start_poses =[(5,5), (5,6), (6,4), (6,7), (7,5), (7,6)] # Row Major
        return self.test_static_from_start_pos(start_poses=start_poses)

    def test_loaf(self) -> bool:
        start_poses = [
            (3,5),(3,6),
            (4,4),(4,7),
            (5,5),(5,7),
            (6,6)]
        return self.test_static_from_start_pos(start_poses=start_poses)

    def test_boat(self) -> bool:
        start_poses = [
            (4,4), (4,5),
            (5,4), (5,6),
            (6,5)
        ]
        return self.test_static_from_start_pos(start_poses=start_poses)

    def test_tub(self) -> bool:
        start_poses = [
            (4,5),
            (5,4), (5,6),
            (6,5)
        ]
        return self.test_static_from_start_pos(start_poses=start_poses)
    
    def test_blinker(self) -> bool:
        start_poses = [(4,5), (5,5), (6,5)]
        final_poses = [(5,4), (5,5), (5,6)]
        return self.test_transformation_from_start_to_final(start_poses, final_poses)

    def test_beacon(self) -> bool:
        start_poses = [
            (4,4), (4,5),
            (5,4), (5,5),
            (6,6), (6,7),
            (7,6), (7,7)]
        final_poses = [
            (4,4), (4,5),
            (5,4), 
            (6,7),
            (7,6), (7,7)]
        return self.test_transformation_from_start_to_final(start_poses, final_poses)

    def test_two_points_together(self) -> bool:
        start_board = np.copy(self.prev_board)
        start_board[(5,5)] = 1
        start_board[(5,6)] = 1
        next = self.run_one_step(start_board)
        return np.array_equal(self.zero_board, next)

    def test_two_points_seperated(self) -> bool: 
        start_board = np.copy(self.prev_board)
        start_board[(2,2)] = 1
        start_board[(8,8)] = 2
        next = self.run_one_step(start_board)
        return np.array_equal(self.zero_board, next)

    def test_single_point(self) -> bool:
        start_board = np.copy(self.prev_board)
        start_pos = (5,5)
        start_board[start_pos] = 1
        next_board = self.run_one_step(start_board)
        return np.array_equal(self.zero_board, next_board)

    def test_empty_board(self) -> bool:
        next_board = self.run_one_step(self.prev_board)
        return np.array_equal(self.zero_board, next_board)

    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.prev_board = np.zeros((self.width, self.height))
        self.zero_board = np.zeros_like(self.prev_board)
        self.next_board = np.zeros_like(self.prev_board)


if __name__ == '__main__':
    test = RulesTesting()
    test.run_all_tests()
