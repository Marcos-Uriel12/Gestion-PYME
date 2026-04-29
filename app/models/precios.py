from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.database import Base

class Precio(Base):
    __tablename__ = "precios"

    id = Column(Integer, primary_key=True, index=True)
    productos_id = Column(Integer, ForeignKey("products.id"))
    precio_BA = Column(Float, nullable=False)
    precio_interior = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
