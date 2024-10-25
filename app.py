import numpy as np
import uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

from utils.algo import Solver
app = FastAPI()

class PuzzleInput(BaseModel):
    tile_map: List[List[str]]
    pellet_map: List[List[str]]
    start_position: tuple
    @field_validator('tile_map', 'target_map')
    def convert_str_to_int(cls, v):
        return [[int(tile) for tile in row] for row in v]

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/solve")
async def solve(puzzle: PuzzleInput):
    tile_map = np.array(puzzle.tile_map)
    pellet_map = np.array(puzzle.pellet_map)
    start_position = puzzle.start_position

    solution = Solver.collect_all_pellets(tile_map, pellet_map, start_position)

    return {
        "solution": solution
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5002, reload=True, reload_dirs=["."])