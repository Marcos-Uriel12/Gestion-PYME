
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.password import get_current_user
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate,CategoriaResponse
from app.models.user import User

router = APIRouter(prefix="/categoria", tags=["categoria"])

@router.post("/", response_model=CategoriaResponse,status_code=201)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if db.query(Categoria).filter(Categoria.tipo == categoria.tipo).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria already exists")
    db_categoria = Categoria(tipo = categoria.tipo)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@router.get("/", response_model=list[CategoriaResponse],status_code=200 )
def get_categorias(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Categoria).all()

@router.delete("/{id}",status_code=204)
def delete_categoria(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not db_categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria not found")
    db.delete(db_categoria)
    db.commit()
    return db_categoria

