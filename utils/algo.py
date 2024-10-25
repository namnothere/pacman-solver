from collections import deque

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

class Solver:
    def __init__(self, grid, start):
        self.grid = grid
        self.start = start

    def bfs(self, grid: list, start, goal):
        queue = deque([(start, [start])])

        return []

    def collect_all_pellets(self, grid: list, pellet_map: list, start: tuple):
        collected_paths = []
        current_position = start

        return collected_paths

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
    collected_paths = solver.collect_all_pellets(grid, pellet_map, start_position)

    print("Collect all pellets path")
    for path in collected_paths:
        print(path)