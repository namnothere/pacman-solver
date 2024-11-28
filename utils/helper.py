import hashlib
import numpy as np

from enum import Enum

from utils.constants import BOARD_SIZE, PLAYER_ANOTATION, WALL

class ALGO(Enum):
    BFS = 0
    DFS = 1
    ID = 2
    UCS = 3
    HC = 4
    GBFS = 5

def direction_to_string(direction):
    if direction == (-1, 0):
        return "Up"
    elif direction == (1, 0):
        return "Down"
    elif direction == (0, 1):
        return "Right"
    elif direction == (0, -1):
        return "Left"
    else:
        return "Invalid direction"

# def get_available_directions(state: list[list], current_pos: tuple):
#     available_directions = []
#     directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#     # empty_cell = np.where(state == PLAYER_ANOTATION)
#     empty_cell = current_pos
#     for i, j in directions:
#         next_pos = (empty_cell[0] + i, empty_cell[1] + j)
#         if next_pos[0] >= 0 and next_pos[0] < BOARD_SIZE and next_pos[1] >= 0 and next_pos[1] < BOARD_SIZE:
#             if state[next_pos[0], next_pos[1]] == WALL: continue
#             available_directions.append((i, j))
#     return available_directions

def get_available_directions(grid: np.ndarray, current_pos: tuple):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    available_moves = []
    for dx, dy in directions:
        nx, ny = current_pos[0] + dx, current_pos[1] + dy
        if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1] and grid[nx, ny] != 0:
            available_moves.append((nx, ny))
    return available_moves

def state2hash(state):
    return hashlib.md5(str(state).encode()).hexdigest()

def swap(state: np.ndarray, empty_cell: tuple, new_cell: tuple):
    empty_cell_val = state[empty_cell[0], empty_cell[1]]
    new_cell_val = state[new_cell[0], new_cell[1]]

    state[empty_cell] = new_cell_val
    state[new_cell] = empty_cell_val

    return state