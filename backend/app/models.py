from pydantic import BaseModel
from typing import List, Optional

class GridRequest(BaseModel):
    dimension: Optional[int] = None
    n: Optional[int] = None
    m: Optional[int] = None
    red: Optional[int] = None
    green: Optional[int] = None
    blue: Optional[int] = None
    block_color: Optional[str] = None
    block_size: Optional[int] = None
    block_count: Optional[int] = None
    constraint_type: str
    periphery_colors: Optional[List[str]] = None
    diagonal_colors: Optional[List[str]] = None
    adjacency_cons: Optional[List[str]] = None
    no_adjacency_cons: Optional[List[str]] = None
    
