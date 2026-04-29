from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.password import get_current_user
from app.models.user import User
from app.models.clientes import Cliente
from app.schemas.clientes import ClienteCreate, ClienteResponse, ClienteUpdate

router = APIRouter(prefix="/cliente", tags=["cliente"])

@router.post("/", response_model=ClienteResponse,status_code=201)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    if db.query(Cliente).filter(Cliente.email == cliente.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente already exists")
    db_cliente = Cliente(
        nombre=cliente.nombre,
        apellido=cliente.apellido,
        email=cliente.email,
        telefono=cliente.telefono,
        direccion=cliente.direccion,
        ciudad=cliente.ciudad,
        codigo_postal=cliente.codigo_postal,
        zona=cliente.zona,
        metodo_pago=cliente.metodo_pago
        )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=list[ClienteResponse],status_code=200)
def get_clientes(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    return db.query(Cliente).all()

@router.get("/{id}", response_model=ClienteResponse,status_code=200)
def get_cliente(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")
    return db_cliente

@router.patch("/{id}", response_model=ClienteResponse,status_code=200)
def update_cliente(id: int, cliente: ClienteUpdate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")
    
    if cliente.email is not None and cliente.email != db_cliente.email:
        if db.query(Cliente).filter(Cliente.email == cliente.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cliente already exists")

    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/{id}",status_code=204)
def delete_cliente(id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not db_cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente not found")
    db.delete(db_cliente)
    db.commit()
    return db_cliente
