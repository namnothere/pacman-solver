import heapq
import numpy as np

from utils.constants import PLAYER_ANOTATION
from utils.helper import get_available_directions, state2hash, swap

grid = [
    [2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

grid = np.array(grid)

start_position = (0, 0)
pellet_map = [(0, 1)]

def greedy():
    initial_state = grid.copy()

    heap = [(0, initial_state, [], pellet_map)]
    visited = set()

    while heap:
        cost, state, path, remaining_pellets = heapq.heappop(heap)
        current_pos = np.where(state == PLAYER_ANOTATION)
        print("Current position", (current_pos[0][0], current_pos[1][0]))
        print("Remaining pellets: ", remaining_pellets)

        new_remaining_pellets = remaining_pellets.copy()
        if tuple(current_pos) in new_remaining_pellets:
            new_remaining_pellets.remove(tuple(current_pos))

        if not remaining_pellets:
            return path
        
        if state2hash(state) in visited:
            continue

        player_cell = np.where(state == PLAYER_ANOTATION)
        visited.add(state2hash(state))

        for i, j in get_available_directions(state):
            direction = (i, j)
            # print("direction", direction)

            cell_to_move = (player_cell[0] + i, player_cell[1] + j)
            print("cell_to_move", (cell_to_move[0][0], cell_to_move[1][0]))
            new_state = swap(state, player_cell, cell_to_move)

            new_heuristic = greedy_heuristic(new_state, new_remaining_pellets)

            heapq.heappush(heap, (new_heuristic, new_state, path + [direction], new_remaining_pellets))

    return []

def greedy_heuristic(state: np.array, remaining_pellets: list):
    if not remaining_pellets:
        return 0
    
    player_cell = np.where(state == PLAYER_ANOTATION)
    player_row, player_col = player_cell[0][0], player_cell[1][0]
    print("Heuristic from ", (player_row, player_col), " to ", remaining_pellets)
    heuristic_list = [abs(player_col - x) + abs(player_row - y) for x, y in remaining_pellets]
    # print(heuristic_list)
    return min(heuristic_list)

collected_paths = greedy()

print("Collect all pellets path")
for path in collected_paths:
    print(path)