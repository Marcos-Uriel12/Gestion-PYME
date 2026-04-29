from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Literal
from typing import Optional

class ClienteCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: str
    codigo_postal: Optional[str] = None
    zona: Literal["Buenos Aires", "Interior"]
    metodo_pago: str

class ClienteResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: str
    codigo_postal: Optional[str] = None
    zona: Literal["Buenos Aires", "Interior"]
    metodo_pago: str
    created_at: datetime
    updated_at: datetime

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    codigo_postal: Optional[str] = None
    zona: Optional[Literal["Buenos Aires", "Interior"]] = None
    metodo_pago: Optional[str] = None
