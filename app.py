import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from typing import List
app = FastAPI()

class PuzzleInput(BaseModel):
    tile_map: List[List[str]]
    target_map: List[List[str]]

    @field_validator('tile_map', 'target_map')
    def convert_str_to_int(cls, v):
        return [[int(tile) for tile in row] for row in v]

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5002, reload=True, reload_dirs=["."])