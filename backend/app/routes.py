from fastapi import APIRouter, HTTPException
from fastapi import Request
from app.models import GridRequest
from pydantic import BaseModel
import google.generativeai as genai
import os
from app.services import fill_grid_periphery, fill_grid_diagonal, adjacency_const, no_adjcol, block_col, patternn

# Load your API key
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="AIzaSyA4fANeT1nJQUrugOyHiQeoU_agk9jkrPQ")

router = APIRouter()

class InputData(BaseModel):
    text: str

prmpt = "print my input again in capital letters {input_text}"

@router.post("/generate-gemini")
async def generate_gemini(data: InputData):
    try:
        input_prompt = prmpt.format(input_text=data.text)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(input_prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-grid")
def generate_grid(request: GridRequest):
    if request.constraint_type == "periphery":
        grid = fill_grid_periphery(request.n, request.m, request.red, request.green, request.blue, request.periphery_colors)
    elif request.constraint_type == "diagonal":
        grid = fill_grid_diagonal(request.dimension, request.red, request.green, request.blue, request.diagonal_colors)
    elif request.constraint_type == "adj_const":
        grid = adjacency_const(request.n, request.m, request.red, request.green, request.blue, request.adjacency_cons) 
    elif request.constraint_type == "no_adj_const":
        grid = no_adjcol(request.n, request.m, request.red, request.green, request.blue)
    elif request.constraint_type == "block":
        grid = block_col(request.n, request.m, request.red, request.green, request.blue, request.block_color, request.block_size, request.block_count)
    elif request.constraint_type == "patternnn":
        grid = patternn(request.n, request.m, request.red, request.green, request.blue, request.pattern_length, request.pattern)
    else:
        return {"error": "Invalid constraint type"}
    
    return {"grid": grid}
