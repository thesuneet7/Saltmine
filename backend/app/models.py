from pydantic import BaseModel
from typing import List, Optional

class GridRequest(BaseModel):
    dimension: int
    red: int
    green: int
    blue: int
    constraint_type: str
    periphery_colors: Optional[List[str]] = None
    diagonal_colors: Optional[List[str]] = None
