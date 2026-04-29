from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class CategoriaCreate(BaseModel):
    tipo: Literal["materia_prima", "producto_terminado"]

class CategoriaResponse(BaseModel):
    id: int
    tipo: Literal["materia_prima", "producto_terminado"]
    created_at: datetime

    class Config:
        from_attributes = True