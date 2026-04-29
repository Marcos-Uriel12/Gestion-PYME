from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.password import get_current_user
from app.models.user import User
from app.models.precios import Precio
from app.schemas.precios import PrecioCreate, PrecioResponse
from app.models.products import Product

router = APIRouter(prefix="/precio", tags=["precio"])

@router.post("/", response_model=PrecioResponse,status_code=201)
def create_precio(precio: PrecioCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if not db.query(Product).filter(Product.id == precio.productos_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    if precio.precio_BA <= 0 or precio.precio_interior <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Los precios deben ser mayores a 0")
    
    precios  = db.query(Precio).filter(Precio.productos_id == precio.productos_id).order_by(Precio.created_at.asc()).all()
    
    if len(precios) >= 3:
        db.delete(precios[0])
        db.commit()
    
    db_precio = Precio(
        precio_BA=precio.precio_BA,
        precio_interior=precio.precio_interior,
        productos_id=precio.productos_id
        )
    db.add(db_precio)
    db.commit()
    db.refresh(db_precio)
    return db_precio

@router.get("/{id}", response_model=PrecioResponse,status_code=200)
def get_precio(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_precio = db.query(Precio).filter(Precio.id == id).first()
    if not db_precio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio no encontrado")
    return db_precio

@router.get("/", response_model=list[PrecioResponse],status_code=200)
def get_precios(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Precio).order_by(Precio.created_at.asc()).all()

@router.delete("/{id}",status_code=204)
def delete_precio(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_precio = db.query(Precio).filter(Precio.id == id).first()
    if not db_precio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio no encontrado")
    db.delete(db_precio)
    db.commit()
    return db_precio