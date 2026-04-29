from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProductoCreate(BaseModel):
    nombre: str
    stock: float
    unidad_medida: Optional[str] = None
    medidas_opcionales: Optional[str] = None
    tipo_mueble: Optional[str] = None
    categoria_id: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    stock: Optional[float] = None
    unidad_medida: Optional[str] = None
    medidas_opcionales: Optional[str] = None
    tipo_mueble: Optional[str] = None
    categoria_id: Optional[int] = None

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    stock: float
    unidad_medida: Optional[str] = None
    medidas_opcionales: Optional[str] = None
    tipo_mueble: Optional[str] = None
    categoria_id: int
    created_at: datetime

    class Config:
        from_attributes = True