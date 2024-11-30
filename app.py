import numpy as np
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

from utils.algo import Solver
from utils.helper import ALGO
app = FastAPI()

class PuzzleInput(BaseModel):
    tile_map: List[List[int]]
    pellet_map: List[List[int]]
    start_position: list
    algo: ALGO = ALGO.BFS

    # @field_validator('tile_map', 'pellet_map', mode="before")
    # def convert_list_str_to_int(cls, v):
    #     return [[int(tile) for tile in row if not isinstance(tile, int)] for row in v]

    @field_validator('pellet_map', mode="after")
    def convert_list_int_to_tuple(cls, v):
        return [tuple(row) for row in v]

    # @field_validator('start_position', mode="before")
    # def convert_str_to_int(cls, v):
    #     return [int(tile) if not isinstance(tile, int) else tile for tile in v]
    
    @field_validator('algo', mode="before")
    def convert_int_to_enum(cls, v):
        if isinstance(v, int):
            return ALGO(v)
        return v

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/solve")
async def solve(puzzle: PuzzleInput):
    tile_map = np.array(puzzle.tile_map)
    pellet_map = puzzle.pellet_map
    start_position = (puzzle.start_position[0], puzzle.start_position[1])
    algo = puzzle.algo

    try:
        res = Solver(tile_map, pellet_map, start_position).collect_all_pellets(algo)
        return res

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred. " + str(e))

@app.get("/test")
async def test():
    grid = [[0,0,0,0,0,0,0,0,0,0,0],[0,-1,0,-1,-1,-1,-1,-1,-1,-1,0],[0,-1,0,0,0,0,0,0,0,-1,0],[0,-1,-1,-1,-1,-1,0,-1,-1,-1,0],[0,0,0,0,0,-1,0,-1,0,-1,0],[0,-1,-1,-1,0,-1,-1,-1,0,-1,0],[0,-1,0,0,0,0,0,0,0,-1,0],[0,-1,1,-1,0,2,-1,-1,-1,-1,0],[0,-1,0,-1,0,-1,0,0,0,0,0],[0,-1,0,-1,-1,-1,-1,-1,-1,-1,0],[0,0,0,0,0,0,0,0,0,0,0]]

    start_position = (0, 0)
    pellet_map = [(7,2)]

    solver = Solver(grid, pellet_map, start_position)
    collected_paths = solver.a_star()

    print("Collect all pellets path")
    for path in collected_paths:
        print(path)

    return {
        "solution": collected_paths
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5005, reload=True, reload_dirs=["."])