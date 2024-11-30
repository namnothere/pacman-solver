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
        if type(result) == dict:
            result["runtime"] = run_time
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
        if algo == ALGO.DFS:
            return self.dfs()
        if algo == ALGO.BFS:
            return self.bfs()
        if algo == ALGO.GBFS:
            return self.greedy()
        if algo == ALGO.UCS:
            return self.ucs()
        if algo == ALGO.ASTAR:
            return self.a_star()
        else:
            raise ValueError("Invalid algorithm")

    # @measure_runtime
    # def greedy(self):
    #     initial_state = self.grid.copy()
    #     raw_state = initial_state.copy()
    #     raw_state[raw_state == PLAYER_ANOTATION] = FLOOR

    #     pellets_map = self.pellet_map.copy()
    #     current_pos = np.argwhere(initial_state == PLAYER_ANOTATION)

    #     if current_pos.size == 0:
    #         print("Player not found in the initial state.")
    #         return None
        
    #     current_pos = tuple(current_pos[0])

    #     remaining_targets = set(pellets_map)
    #     reached_targets = []
        
    #     open_list = []
    #     heapq.heappush(open_list, (self.greedy_heuristic(current_pos, pellets_map), current_pos, initial_state, [[int(current_pos[0]), int(current_pos[1])]]))
        
    #     visited = set()        

    #     while open_list and remaining_targets:
    #         _, current_pos, current_state, path = heapq.heappop(open_list)

    #         print("Current state\n", current_state)
    #         print("current_pos", current_pos)
            
    #         if current_pos not in visited:
    #             visited.add(current_pos)
    #         if current_pos in remaining_targets:
    #             print(f"Target {current_pos} reached!")
    #             remaining_targets.remove(current_pos)
    #             reached_targets.append(current_pos)

    #         if not remaining_targets:
    #             print(f"All targets reached: {reached_targets}")
    #             return path + [[int(current_pos[0]), int(current_pos[1])]]

    #         available_directions = get_available_directions(current_state)
    #         if not available_directions:
    #             print(f"Dead-end at {current_pos}. Backtracking...")
    #             continue

    #         for direction in available_directions:
    #             next_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
    #             if next_pos not in visited:
    #                 new_state = raw_state.copy()
    #                 new_state[current_pos[0], current_pos[1]] = FLOOR
    #                 new_state[next_pos[0], next_pos[1]] = PLAYER_ANOTATION
    #                 heapq.heappush(open_list, (self.greedy_heuristic(next_pos, remaining_targets), next_pos, new_state, path + [[int(next_pos[0]), int(next_pos[1])]]))
        
    #     if not remaining_targets:
    #         print(f"All targets reached: {reached_targets}")
    #         return path
    #     else:
    #         print(f"Not all targets reached. Remaining: {remaining_targets}")
    #         return None

    # def greedy_heuristic(self, current_pos, remaining_pellets: list):
    #     if not remaining_pellets:
    #         return float('inf')
    #     heuristic_list = [(abs(current_pos[0] - pellet[0]) + abs(current_pos[1] - pellet[1])) for pellet in remaining_pellets]
    #     return min(heuristic_list)

    def greedy_heuristic(self, current, target):
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

    def get_player_coords(self, grid):
        player_coords = np.argwhere(grid == 2)
        if player_coords.size == 0:
            raise ValueError("Player not found on the grid.")
        return tuple(player_coords[0]) # (row, col)

    @measure_runtime
    def greedy(self):
        initial_state = self.grid.copy()
        pellet_map = self.pellet_map.copy()
        player_pos = self.get_player_coords(initial_state)
        remaining_targets = set(pellet_map)
        path = []

        while remaining_targets:
            closest_target = min(remaining_targets, key=lambda t: self.greedy_heuristic(player_pos, t))
            open_list = [(self.greedy_heuristic(player_pos, closest_target), player_pos)]
            came_from = {player_pos: None}
            visited = set()
            found_path = False

            while open_list:
                _, current_pos = heapq.heappop(open_list)

                if current_pos in visited:
                    continue
                visited.add(current_pos)

                if current_pos == closest_target:
                    print(f"Target {closest_target} reached!")
                    temp_pos = current_pos
                    target_path = []
                    while temp_pos:
                        target_path.append(temp_pos)
                        temp_pos = came_from[temp_pos]
                    target_path.reverse()
                    path.extend(target_path[1:])
                    player_pos = closest_target
                    remaining_targets.remove(current_pos)
                    found_path = True
                    break

                for next_pos in get_available_directions(initial_state, current_pos):
                    if next_pos not in visited and next_pos not in came_from:
                        heapq.heappush(open_list, (self.greedy_heuristic(next_pos, closest_target), next_pos))
                        came_from[next_pos] = current_pos

            if not found_path:
                print(f"No path found to target {closest_target}.")
                remaining_targets.remove(closest_target)

        path = [[int(pos[0]), int(pos[1])] for pos in path]
        print(f"Collect all pellets path: {path}")
        return {
            "solution": path
        }

    @measure_runtime
    def ucs(self):
        initial_state = self.grid.copy()
        pellet_map = self.pellet_map.copy()
        player_pos = self.get_player_coords(initial_state)
        
        total_path = []
        unreachable_targets = []
        remaining_targets = set(pellet_map)
        
        print("UCS")
        while remaining_targets:
            open_list = []
            heapq.heappush(open_list, (0, player_pos, [player_pos]))
            
            visited = set()
            visited.add(player_pos)
            
            found_path = False

            while open_list:
                current_cost, current_pos, current_path = heapq.heappop(open_list)

                if current_pos in remaining_targets:
                    total_path.extend(current_path[1:])
                    player_pos = current_pos
                    remaining_targets.remove(current_pos)
                    found_path = True
                    break

                for neighbor in get_available_directions(initial_state, current_pos):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        new_cost = current_cost + 1
                        new_path = current_path + [neighbor]
                        heapq.heappush(open_list, (new_cost, neighbor, new_path))
            
            if not found_path:
                unreachable_targets.append(player_pos)
                break

        if unreachable_targets:
            unreachable_targets_str = ', '.join([str(t) for t in unreachable_targets])
            print({'unreachable_targets': unreachable_targets_str, 'solution': total_path})
            total_path = [[int(pos[0]), int(pos[1])] for pos in total_path]
            return {
                'unreachable_targets': unreachable_targets_str,
                'solution': total_path
            }
        
        # return {
        #     'unreachable_targets': None,
        #     'solution': total_path
        # }
        total_path = [[int(pos[0]), int(pos[1])] for pos in total_path]
        # return total_path
        return {
            'unreachable_targets': None,
            'solution': total_path
        }
    

    @measure_runtime
    def bfs(self):
        initial_state = self.grid.copy()
        pellet_map = self.pellet_map.copy()
        player_pos = self.get_player_coords(initial_state)
    
        queue = deque([(player_pos, [])])
        visited = set()
        visited.add(player_pos)
        path = []

        while queue:
            current_pos, current_path = queue.popleft()

            if current_pos in pellet_map:
                pellet_map.remove(current_pos)
                path.extend(current_path + [current_pos])
                if not pellet_map:
                    break

            for neighbor in get_available_directions(initial_state, current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, current_path + [neighbor]))
    
        path = [[int(pos[0]), int(pos[1])] for pos in path]
        return {"solution": path}

    @measure_runtime
    def dfs(self):
        initial_state = self.grid.copy()
        pellet_map = self.pellet_map.copy()
        player_pos = self.get_player_coords(initial_state)
    
        stack = [(player_pos, [])]
        visited = set()
        visited.add(player_pos)
        path = []

        while stack:
            current_pos, current_path = stack.pop()

            if current_pos in pellet_map:
                pellet_map.remove(current_pos)
                path.extend(current_path + [current_pos])
                if not pellet_map:
                    break

            for neighbor in get_available_directions(initial_state, current_pos):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, current_path + [neighbor]))
    
        path = [[int(pos[0]), int(pos[1])] for pos in path]
        return {"solution": path}


    @measure_runtime
    def a_star(self):
        initial_state = self.grid.copy()
        pellet_map = self.pellet_map.copy()
        player_pos = self.get_player_coords(initial_state)
        remaining_targets = set(pellet_map)
        path = []
        
        while remaining_targets:
            closest_target = min(remaining_targets, key=lambda t: self.a_star_heuristic(player_pos, t))
            open_list = [(0 + self.a_star_heuristic(player_pos, closest_target), 0, player_pos, [])]  # (f, g, current_pos, path)
            came_from = {player_pos: None}
            visited = set()

            while open_list:
                f, g, current_pos, current_path = heapq.heappop(open_list)

                if current_pos in visited:
                    continue
                visited.add(current_pos)

                # If we reach the target, reconstruct the path
                if current_pos == closest_target:
                    print(f"Target {closest_target} reached!")
                    temp_pos = current_pos
                    target_path = []
                    while temp_pos:
                        target_path.append(temp_pos)
                        temp_pos = came_from[temp_pos]
                    target_path.reverse()
                    path.extend(target_path[1:])
                    player_pos = closest_target
                    remaining_targets.remove(current_pos)
                    break

                # Explore neighbors
                for next_pos in get_available_directions(initial_state, current_pos):
                    if next_pos not in visited:
                        new_g = g + 1  # Uniform cost of 1 for each step
                        heapq.heappush(open_list, (
                            new_g + self.a_star_heuristic(next_pos, closest_target),  # f = g + h
                            new_g,
                            next_pos,
                            current_path + [current_pos]
                        ))
                        came_from[next_pos] = current_pos

        path = [[int(pos[0]), int(pos[1])] for pos in path]
        print(f"A* path to collect all pellets: {path}")
        return {
            "solution": path
        }
    def a_star_heuristic(self, current, target):
        return abs(current[0] - target[0]) + abs(current[1] - target[1])

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
    collected_paths = solver.greedy()

    print("Collect all pellets path")
    for path in collected_paths:
        print(path)