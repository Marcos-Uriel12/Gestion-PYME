from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    stock = Column(Float, nullable=False)
    unidad_medida = Column(String(20))
    medidas_opcionales = Column(String(20))
    tipo_mueble = Column(String(20))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
