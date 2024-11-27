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

def get_available_directions(state: list[list]):
    available_directions = []
    empty_cell = np.where(state == PLAYER_ANOTATION)
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_pos = (empty_cell[0] + i, empty_cell[1] + j)
        if next_pos[0] >= 0 and next_pos[0] < BOARD_SIZE and next_pos[1] >= 0 and next_pos[1] < BOARD_SIZE:
            if state[next_pos[0], next_pos[1]] == WALL: continue
            available_directions.append((i, j))
    return available_directions

def state2hash(state):
    return hashlib.md5(str(state).encode()).hexdigest()

def swap(state: np.ndarray, empty_cell: tuple, new_cell: tuple):
    empty_cell_val = state[empty_cell[0], empty_cell[1]]
    new_cell_val = state[new_cell[0], new_cell[1]]

    state[empty_cell] = new_cell_val
    state[new_cell] = empty_cell_val

    return state