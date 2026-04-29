from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum("materia_prima", "producto_terminado", name="tipo_categoria"), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))