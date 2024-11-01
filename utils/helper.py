from enum import Enum
import numpy as np

BOARD_SIZE = 25

class ALGO(Enum):
    BFS = 0
    DFS = 1
    ID = 2
    UCS = 3
    HC = 4

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
    empty_cell = np.where(state == 0)
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if empty_cell[0] + i >= 0 and empty_cell[0] + i < BOARD_SIZE and empty_cell[1] + j >= 0 and empty_cell[1] + j < BOARD_SIZE:
            available_directions.append((i, j))
    return available_directions