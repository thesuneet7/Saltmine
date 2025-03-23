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
    pattern_length: Optional[int] = None
    color_counts: Optional[dict] = None
    periphery_order: Optional[List[str]] = None
    non_adjacent: Optional[bool] = None
    constraint_type: str
    periphery_colors: Optional[List[str]] = None
    adjacent_tiles: Optional[List[str]] = None
    diagonal_colors: Optional[List[str]] = None
    adjacency_cons: Optional[List[str]] = None
    no_adjacency_cons: Optional[List[str]] = None
    pattern: Optional[List[str]] = None
    periphery_nonadj: Optional[List[str]] = None
    constraint_priority:  Optional[str] = None
    
