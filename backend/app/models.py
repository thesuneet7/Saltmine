from pydantic import BaseModel
from typing import List, Optional

class GridRequest(BaseModel):
    dimension: Optional[int] = None
    n: Optional[int] = None
    m: Optional[int] = None
    red: int
    green: int
    blue: int
    constraint_type: str
    periphery_colors: Optional[List[str]] = None
    diagonal_colors: Optional[List[str]] = None
    adjacency_cons: Optional[List[str]] = None
