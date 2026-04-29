from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from typing import Optional
from datetime import timezone
from typing import List


class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int

class PedidoItemResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

    class Config:
        from_attributes = True


class PedidoCreate(BaseModel):
    cliente_id: int
    fecha_pedido: datetime = datetime.now(timezone.utc)
    estado: Literal["pendiente", "en_proceso", "enviado", "entregado", "cancelado"]
    items: List[PedidoItemCreate]
    metodo_pago: str

class PedidoUpdate(BaseModel):
    estado: Literal["pendiente", "en_proceso", "enviado", "entregado", "cancelado"]
    metodo_pago: str

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_pedido: datetime
    estado: Literal["pendiente", "en_proceso", "enviado", "entregado", "cancelado"]
    items: List[PedidoItemResponse]
    metodo_pago: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True