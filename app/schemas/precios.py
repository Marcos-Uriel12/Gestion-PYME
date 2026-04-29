from pydantic import BaseModel
from datetime import datetime


class PrecioCreate(BaseModel):
    precio_BA: float
    precio_interior: float
    productos_id: int

class PrecioResponse(BaseModel):
    id: int
    precio_BA: float
    precio_interior: float
    productos_id: int
    created_at: datetime
    updated_at: datetime
class Config:
    from_attributes = True