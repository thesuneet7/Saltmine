from fastapi import APIRouter
from app.models import GridRequest
from app.services import fill_grid_periphery, fill_grid_diagonal

router = APIRouter()

@router.post("/generate-grid")
def generate_grid(request: GridRequest):
    if request.constraint_type == "periphery":
        grid = fill_grid_periphery(request.dimension, request.red, request.green, request.blue, request.periphery_colors)
    elif request.constraint_type == "diagonal":
        grid = fill_grid_diagonal(request.dimension, request.red, request.green, request.blue, request.diagonal_colors)
    else:
        return {"error": "Invalid constraint type"}
    
    return {"grid": grid}
