from fastapi import APIRouter, HTTPException
from fastapi import Request
from app.models import GridRequest
from app.services import fill_grid_periphery, fill_grid_diagonal, adjacency_const, no_adjcol

router = APIRouter()

@router.post("/generate-grid")
def generate_grid(request: GridRequest):
    if request.constraint_type == "periphery":
        grid = fill_grid_periphery(request.dimension, request.red, request.green, request.blue, request.periphery_colors)
    elif request.constraint_type == "diagonal":
        grid = fill_grid_diagonal(request.dimension, request.red, request.green, request.blue, request.diagonal_colors)
    elif request.constraint_type == "adj_const":
        grid = adjacency_const(request.n, request.m, request.red, request.green, request.blue, request.adjacency_cons)
    elif request.constraint_type == "no_adj_const":
        grid = no_adjcol(request.n, request.m, request.red, request.green, request.blue) 
    else:
        return {"error": "Invalid constraint type"}
    
    return {"grid": grid}
