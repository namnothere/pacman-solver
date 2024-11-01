from collections import deque

from utils.helper import ALGO, direction_to_string

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Solver:
    def __init__(self, grid: list[list], pellet_map: list[list], start: tuple):
        self.grid = grid
        self.pellet_map = pellet_map
        self.start = start

    def bfs(self, grid: list, pellet_map: list[list], start: tuple):
        queue = deque([(grid, [])])
        state, path = queue.popleft()
        return path + [direction_to_string((-1, 0))]
    
    def collect_all_pellets(self, algo: ALGO.BFS):
        if algo == ALGO.BFS:
            return self.bfs(self.grid, self.pellet_map, self.start)
        else:
            raise ValueError("Invalid algorithm")
            

if __name__ == "__main__":
    grid = [
        [0, 0, 0, 1, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 2, 0],
        [0, 1, 1, 1, 0],
        [2, 0, 0, 0, 0]
    ]

    start_position = (0, 0)
    pellet_map = [(1, 2), (2, 3), (4, 0)]

    solver = Solver(grid, start_position)
    collected_paths = solver.bfs(grid, pellet_map, start_position)

    print("Collect all pellets path")
    for path in collected_paths:
        print(path)