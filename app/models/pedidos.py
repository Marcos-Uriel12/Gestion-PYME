from http import client
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    fecha_pedido = Column(DateTime, default=datetime.now(timezone.utc))
    estado = Column(Enum("pendiente", "en_proceso", "enviado", "entregado", "cancelado", name="estado_pedido"), nullable=False)
    metodo_pago = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    cliente = relationship("Cliente", back_populates="pedidos")
    items = relationship("PedidoItems", back_populates="pedido")

class PedidoItems(Base):
    __tablename__ = "pedidoItem"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    producto_id = Column(Integer, ForeignKey("products.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    pedido = relationship("Pedido", back_populates="items")