import numpy as np
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

from utils.algo import Solver
from utils.helper import ALGO
app = FastAPI()

class PuzzleInput(BaseModel):
    tile_map: List[List[str]]
    pellet_map: List[List[str]]
    start_position: list
    algo: ALGO = ALGO.BFS

    @field_validator('tile_map', 'pellet_map', mode="before")
    def convert_list_str_to_int(cls, v):
        return [[int(tile) for tile in row if not isinstance(tile, int)] for row in v]

    @field_validator('start_position', mode="before")
    def convert_str_to_int(cls, v):
        return [int(tile) if not isinstance(tile, int) else tile for tile in v]
    
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
    pellet_map = np.array(puzzle.pellet_map)
    print(puzzle.start_position)
    start_position = (puzzle.start_position[0], puzzle.start_position[1])
    algo = puzzle.algo

    try:
        solution = Solver(tile_map, pellet_map, start_position).collect_all_pellets(algo)

        return {
            "solution": solution
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error occurred. " + str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5005, reload=True, reload_dirs=["."])