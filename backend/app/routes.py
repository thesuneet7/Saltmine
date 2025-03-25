from fastapi import APIRouter, HTTPException
from fastapi import Request
from app.models import GridRequest
from pydantic import BaseModel
import google.generativeai as genai
import os
from app.services import fill_grid_periphery, fill_grid_diagonal, adjacency_const, no_adjcol, block_col, patternn, diagonal_periphery_pattern, diagonal_adj, periphery_bb, diagonal_periphery_priority, periphery_pattern, periphery_nonadj, adj_dia_peri


# Load your API key
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key="AIzaSyA4fANeT1nJQUrugOyHiQeoU_agk9jkrPQ")

router = APIRouter()

class InputData(BaseModel):
    text: str

prmpt = '''The set of algorithms can be utilized by a workspace design company to optimize office layouts. Here, the grid represents the floor of a company, where different occupations—such as engineers, architects, and designers—are symbolized by R, G, and B. By using these codes, the company can strategically allocate workspaces. Each algorithm follows a specific strategy for floor planning, allowing the company to choose the one that best aligns with their workspace requirements, whether it's maximizing collaboration, minimizing disruptions, or balancing different departments efficiently.To achieve this, the company can implement various constraints based on its design objectives:
●	Diagonal Constraint – Ensures that specific roles are placed diagonally for better workflow.
●	Periphery Constraint – Allocates certain occupations to the edges of the workspace for accessibility or separation.
●	Adjacency Constraint – Prevents two adjacent tiles from having the same occupation to promote diversity in team placement.
●	Big Colored Block Constraint – Clusters similar roles together to create focused work zones.
●	Pattern Constraint – Ensures a predefined repeating pattern in the layout.
●	Weighted Positional Constraint – Assigns different importance levels to specific locations for optimized placement.


Diagonal Constraint - 
This program systematically places elements along the diagonals of a grid based on predefined priorities, ensuring controlled placement. The remaining positions are then filled randomly while maintaining the specified quantities of each element. This approach ensures a structured yet flexible distribution within the grid.

Periphery Constraint- 
This program strategically places elements along the periphery of a grid based on predefined priorities, ensuring controlled placement. The remaining positions within the grid are then filled randomly while maintaining the specified quantities of each element. This approach allows for structured yet flexible distribution, making it suitable for applications where boundary emphasis is required.
Adjacency Constraint - 
This program strategically places elements within a grid while enforcing adjacency constraints between two selected elements. It ensures that the specified tiles appear adjacent in a balanced manner, prioritizing structured placement. The remaining positions are then filled randomly while maintaining the required quantities of each element. This approach enables controlled yet flexible spatial distribution, making it useful for applications requiring adjacency-based placement.
No two adjacent tiles can have the same color - 
This program generates a structured grid where no two adjacent tiles share the same color, ensuring controlled spatial distribution. This approach makes it useful for applications requiring adjacency-based placement.
Big Coloured Block- 
This program strategically places square blocks of a specified size and color within a grid while ensuring that the total tile distribution remains accurate. After placing the required blocks, the remaining spaces are filled randomly, maintaining the specified tile counts. This method is useful for applications requiring structured block placement alongside randomized distribution.
Pattern Constraint- 
This program efficiently generates a structured grid by strategically placing user-defined tile patterns while ensuring the exact distribution of available tiles. Any remaining spaces are populated randomly while maintaining the specified tile distribution. This approach is useful for applications requiring structured pattern repetition with controlled randomness. This program is a better version of adjacency as it could be used to maintain communication for more than two roles.
Weighted Positional Constraint -
This code efficiently places user-defined colors in a grid by prioritizing both optimal quadrant placement and synergy with neighboring cells. It assigns colors based on a weighted probability distribution, ensuring they are placed in the most suitable quadrant while also maximizing adjacency preferences. By balancing these two factors simultaneously, the algorithm optimizes the overall color distribution, ensuring that each cell is positioned in the best possible location with the most favorable neighbors.
Periphery & Non-adjacent Constraint
This program places elements along a grid’s periphery in a user-defined order, ensuring controlled edge placement. It then fills the interior, optionally enforcing non-adjacency to avoid identical neighboring tiles, promoting diversity. This approach blends structured boundaries with flexible interior placement, supporting collaboration and balanced distribution.
 
Periphery & Big Colour Constraint
This program places elements along a grid’s periphery in a user-specified order, ensuring controlled edge placement. It then adds large, square blocks of a chosen color inside, clustering roles into focused zones while respecting color counts. Remaining spaces are filled randomly, combining boundary control with efficient space use.
 
Periphery & Pattern Constraint
This program places elements along a grid’s periphery in a user-specified order, ensuring controlled edge placement. It then applies a user-defined pattern of colors (e.g., RRGB) across interior rows, repeating it as many times as color counts allow, while maintaining exact tile distribution. Remaining spaces are filled randomly, blending structured boundary control with patterned consistency for efficient workspace design.
 
Diagonal & Periphery & Pattern Constraint
This program places elements along a square grid’s periphery and diagonals (main and anti-diagonal) in user-specified color patterns, ensuring controlled placement at edges and diagonal lines. It prioritizes these patterns using available color counts (R, G, B), then fills remaining spaces randomly while maintaining the exact tile distribution. This approach blends structured boundary and diagonal organization with flexible interior placement for balanced workspace design.

Periphery & Diagonal Constraint (Priority)
This program fills a square grid by prioritizing either periphery or diagonal placement (main and anti-diagonal) based on user choice, using specified color patterns (R, G, B) for each. It applies the higher-priority constraint first, ensuring controlled placement along edges or diagonals, then fills the lower-priority area and remaining spaces randomly while respecting color counts. This flexible, priority-driven approach balances structured layout with adaptability for workspace optimization.

Diagonal & Adjacency Constraint
This program places user-specified colors (R, G, B) along a square grid’s main and anti-diagonals in a given order, ensuring controlled diagonal placement. It then fills the remaining spaces, enforcing adjacency between two selected colors while preventing other tiles from having multiple identical neighbors, promoting balanced diversity. This combines structured diagonal organization with adjacency-driven placement for effective workspace layouts.

Adjacency + Periphery + Diagonal Constraint
This program places colors (R, G, B) along a square grid’s periphery and diagonals (main and anti-diagonal) in user-specified orders, ensuring controlled edge and diagonal placement. It then enforces adjacency between two chosen colors while preventing excessive identical neighbors elsewhere, filling remaining spaces randomly. This integrates structured boundaries and diagonals with adjacency-driven diversity for optimized workspace layouts.

Example input: 
Q. I want to design a floor plan such that all types of occupation groups get a chance to interact with each other. I do not want people of the same occupation sitting in a group and just acting like chauvinists. I want all architects, engineers, and design people to bond and work effectively.

Answer – "Choose the “No two adjacent” constraint and give your specified inputs"
the answer could also be combination of constraints as stated above (not necessary always).
Only answer what constraint to choose in two sentences.
Actual Input: 
 {input_text}'''

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
    elif request.constraint_type == "diagonal_adj_const":
        grid = diagonal_adj(request.dimension, request.red, request.green, request.blue, request.diagonal_colors, request.adjacency_cons)
    elif request.constraint_type == "periphery_bb_const":
        grid = periphery_bb(request.n, request.m, request.red, request.green, request.blue, request.periphery_colors, request.block_color, request.block_size, request.block_count)
    elif request.constraint_type == "dpp1_const":
        grid = diagonal_periphery_pattern(request.dimension, request.red, request.green, request.blue, request.periphery_colors, request.diagonal_colors)
    elif request.constraint_type == "dpp2_const":
        grid = diagonal_periphery_priority(request.dimension, request.red, request.green, request.blue, request.periphery_colors, request.diagonal_colors, request.constraint_priority)
    elif request.constraint_type == "periphery_pattern_const":
        grid = periphery_pattern(request.n, request.m, request.red, request.green, request.blue, request.periphery_colors, request.pattern_length, request.pattern)
    elif request.constraint_type == "periphery_nadj_const":
        grid = periphery_nonadj(request.n, request.m, request.red, request.green, request.blue, request.periphery_colors)
    elif request.constraint_type == "adp_const":
        grid = adj_dia_peri(request.dimension, request.red, request.green, request.blue, request.periphery_colors, request.diagonal_colors, request.adjacent_tiles)
    else:
        return {"error": "Invalid constraint type"}
    
    return {"grid": grid}
