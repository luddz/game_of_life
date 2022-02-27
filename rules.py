import numpy as np

class GameOfLife:
    # Check if a alive cell should continue to live or not based on the following three rules
    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    # Any live cell with two or three live neighbours lives on to the next generation.
    # Any live cell with more than three live neighbours dies, as if by overpopulation.
    # @return: true if it should live and false if it should die
    def check_alive_cell(self, alive_neighbours:int, is_alive:bool) -> bool:
        return is_alive and 3 >= alive_neighbours >= 2

    # Chek if a dead cell should be resourected by the folliwing rule.
    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    def check_dead_cell(self, alive_neighbours:int, is_alive:bool) -> bool:
        return not is_alive and alive_neighbours == 3

    def check_rules(self, state, position) -> bool:
        alive_neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                test_x = position[0] + i
                test_y = position[1] + j
                # Check so we are not checking our own position and OB checks.
                if (test_x, test_y) == position  or test_x < 0 or test_x >= state.shape[0] or test_y < 0 or test_y >= state.shape[1]:
                    continue
        
                if state[(test_x, test_y)] == 1:
                    alive_neighbours += 1

                ## Optimization, due to no cell with more than three alive neighbours will live.
                if alive_neighbours > 3:
                    return False 

        is_alive = state[(position)] == 1 
        return self.check_alive_cell(alive_neighbours, is_alive) or self.check_dead_cell(alive_neighbours, is_alive)
    
    def run_one_step(self) -> np.array:
        next_board = np.zeros_like(self.state)
        for row_n, row in enumerate(self.state):
            for column_n, _ in enumerate(row):
                next_board[row_n][column_n] = 1 if self.check_rules(self.state, (row_n, column_n)) else 0

        self.state = next_board
        return next_board

    def set_start_pos(self, start_poses:np.array) -> None:
        self.state = np.zeros_like(self.state) # Clear the current state of the game
        for pos in start_poses:
            self.state[pos] = 1

    def __init__(self, w:int, h:int,) -> None:
        self.width = w
        self.height = h
        self.state = np.zeros((self.width, self.height))


class RulesTesting:
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

    def zero_from_start_pos(self, start_poses):
        self.gol.set_start_pos(start_poses)
        goal_state = np.zeros_like(self.gol.state)
        return np.array_equal(goal_state, self.gol.run_one_step())

    def static_from_start_pos(self, start_poses):
        self.gol.set_start_pos(start_poses)
        start_board = np.copy(self.gol.state) # Get the orignal state.
        return np.array_equal(start_board , self.gol.run_one_step())
    
    def transformation_from_start_to_final(self, start_poses, final_poses):
        self.gol.set_start_pos(start_poses)
        goal_board = np.zeros_like(self.gol.state)
        for pos in final_poses:
            goal_board[pos] = 1
        
        return np.array_equal(goal_board , self.gol.run_one_step())

    def test_block(self) -> bool:
        start_poses = [ (5,5), (6,5), (5,6), (6,6) ]
        return self.static_from_start_pos(start_poses)

    def test_bee_hive(self) -> bool:
        start_poses =[ (5,5), (5,6), (6,4), (6,7), (7,5), (7,6) ] # Row Major
        return self.static_from_start_pos(start_poses)

    def test_loaf(self) -> bool:
        start_poses = [ (3,5),(3,6), (4,4),(4,7), (5,5),(5,7), (6,6) ]
        return self.static_from_start_pos(start_poses)

    def test_boat(self) -> bool:
        start_poses = [ (4,4), (4,5), (5,4), (5,6), (6,5) ]
        return self.static_from_start_pos(start_poses)

    def test_tub(self) -> bool:
        start_poses = [ (4,5), (5,4), (5,6), (6,5) ]
        return self.static_from_start_pos(start_poses)
    
    def test_blinker(self) -> bool:
        start_poses = [ (4,5), (5,5), (6,5) ]
        final_poses = [ (5,4), (5,5), (5,6) ]
        return self.transformation_from_start_to_final(start_poses, final_poses)

    def test_beacon(self) -> bool:
        start_poses = [ (4,4), (4,5), (5,4), (5,5), (6,6), (6,7), (7,6), (7,7) ]
        final_poses = [ (4,4), (4,5), (5,4), (6,7), (7,6), (7,7) ]
        return self.transformation_from_start_to_final(start_poses, final_poses)

    def test_two_points_together(self) -> bool:
        start_poses = [ (5,5), (5,6) ]
        return self.zero_from_start_pos(start_poses)

    def test_two_points_seperated(self) -> bool: 
        start_poses = [ (2,2), (8,8) ]
        return self.zero_from_start_pos(start_poses)

    def test_single_point(self) -> bool:
        start_pos = [ (5,5) ]
        return self.zero_from_start_pos(start_pos)

    def test_empty_board(self) -> bool:
        start_pos = []
        return self.zero_from_start_pos(start_pos)

    def __init__(self) -> None:
        self.width = 10
        self.height = 10
        self.gol = GameOfLife(self.width, self.height)


if __name__ == '__main__':
    test = RulesTesting()
    test.run_all_tests()
