import time
import numpy as np
import heapq

from collections import deque
from utils.constants import FLOOR, PLAYER_ANOTATION
from utils.helper import ALGO, direction_to_string, get_available_directions, state2hash, swap

def measure_runtime(func):
  def wrapper(*args, **kwargs):
      start_time = time.time()
      result = func(*args, **kwargs)
      end_time = time.time()
      
      run_time = end_time - start_time
      print(f"Function {func.__name__} executed in {run_time:.4f} seconds")
      return result
  return wrapper

class Solver:
    def __init__(self, grid: list[list], pellet_map: list[list], start: tuple):
        # self.grid = np.array(grid)
        self.grid = np.array(grid)
        self.pellet_map = pellet_map
        self.start = start

    def bfs(self, grid: list, pellet_map: list[list], start: tuple):
        queue = deque([(grid, [])])
        state, path = queue.popleft()
        return path + [direction_to_string((-1, 0))]
    
    def collect_all_pellets(self, algo: ALGO.BFS):
        if algo == ALGO.BFS:
            return self.bfs(self.grid, self.pellet_map, self.start)
        if algo == ALGO.GBFS:
            return self.greedy()
        else:
            raise ValueError("Invalid algorithm")

    @measure_runtime
    def greedy(self):
        initial_state = self.grid.copy()
        raw_state = initial_state.copy()
        raw_state[raw_state == PLAYER_ANOTATION] = FLOOR

        pellets_map = self.pellet_map.copy()
        current_pos = np.argwhere(initial_state == PLAYER_ANOTATION)

        if current_pos.size == 0:
            print("Player not found in the initial state.")
            return None
        
        current_pos = tuple(current_pos[0])

        remaining_targets = set(pellets_map)
        reached_targets = []
        
        open_list = []
        heapq.heappush(open_list, (self.greedy_heuristic(current_pos, pellets_map), current_pos, initial_state, [[int(current_pos[0]), int(current_pos[1])]]))
        
        visited = set()        
        
        while open_list and remaining_targets:
            _, current_pos, current_state, path = heapq.heappop(open_list)


            print("Current state\n", current_state)
            print("current_pos", current_pos)
            
            if current_pos not in visited:
                visited.add(current_pos)
            if current_pos in remaining_targets:
                print(f"Target {current_pos} reached!")
                remaining_targets.remove(current_pos)
                reached_targets.append(current_pos)

            if not remaining_targets:
                print(f"All targets reached: {reached_targets}")
                return path + [[int(current_pos[0]), int(current_pos[1])]]

            available_directions = get_available_directions(current_state)
            if not available_directions:
                print(f"Dead-end at {current_pos}. Backtracking...")
                continue

            for direction in available_directions:
                next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
                if next_pos not in visited:
                    new_state = raw_state.copy()
                    new_state[current_pos[0], current_pos[1]] = FLOOR
                    new_state[next_pos[0], next_pos[1]] = PLAYER_ANOTATION
                    heapq.heappush(open_list, (self.greedy_heuristic(next_pos, remaining_targets), next_pos, new_state, path + [[int(next_pos[0]), int(next_pos[1])]]))
        
        if not remaining_targets:
            print(f"All targets reached: {reached_targets}")
            return path
        else:
            print(f"Not all targets reached. Remaining: {remaining_targets}")
            return None

    def greedy_heuristic(self, current_pos, remaining_pellets: list):
        if not remaining_pellets:
            return float('inf')
        heuristic_list = [(abs(current_pos[0] - pellet[0]) + abs(current_pos[1] - pellet[1])) for pellet in remaining_pellets]
        return min(heuristic_list)

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
    # collected_paths = solver.bfs(grid, pellet_map, start_position)
    collected_paths = solver.greedy()

    print("Collect all pellets path")
    for path in collected_paths:
        print(path)