
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.password import get_current_user
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate,CategoriaResponse
from app.models.user import User
from app.models.products import Product
from app.schemas.productos import ProductoCreate, ProductoResponse, ProductoUpdate

router = APIRouter(prefix="/producto", tags=["producto"])

@router.post("/", response_model=ProductoResponse,status_code=201)
def create_producto(producto: ProductoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Categoria).filter(Categoria.id == producto.categoria_id).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria not found")
    
    db_producto = Product(
        nombre=producto.nombre,
        stock=producto.stock, 
        unidad_medida=producto.unidad_medida, 
        medidas_opcionales=producto.medidas_opcionales, 
        tipo_mueble=producto.tipo_mueble, 
        categoria_id=producto.categoria_id)
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/", response_model=list[ProductoResponse],status_code=200)
def get_productos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Product).all()

@router.get("/{id}", response_model=ProductoResponse,status_code=200)
def get_producto(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_producto = db.query(Product).filter(Product.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found")
    return db_producto

@router.delete("/{id}",status_code=204)
def delete_producto(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_producto = db.query(Product).filter(Product.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found")
    db.delete(db_producto)
    db.commit()
    return db_producto

@router.patch("/{id}", response_model=ProductoResponse,status_code=200)
def update_producto(id: int, producto: ProductoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_producto = db.query(Product).filter(Product.id == id).first()
    if not db_producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto not found")
    
    if producto.categoria_id is not None:
        if db.query(Categoria).filter(Categoria.id == producto.categoria_id).first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria not found")
        
    for key, value in producto.model_dump(exclude_unset=True).items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto



