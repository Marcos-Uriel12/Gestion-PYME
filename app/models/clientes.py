from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    ciudad = Column(String(100), nullable=False)
    codigo_postal = Column(String(20))
    zona = Column(Enum("Buenos Aires", "Interior", name="zona"), nullable=False)
    metodo_pago = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    pedidos = relationship("Pedido", back_populates="cliente")