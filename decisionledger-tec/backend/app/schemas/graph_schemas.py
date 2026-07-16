from pydantic import BaseModel
from typing import List, Optional

class GraphNode(BaseModel):
    id: str
    type: str  # 'transaction' | 'customer' | 'account' | 'device' | 'ip' | 'merchant' | 'alert'
    label: str
    risk: str  # 'low' | 'medium' | 'high'
    description: Optional[str] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship: str

class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
