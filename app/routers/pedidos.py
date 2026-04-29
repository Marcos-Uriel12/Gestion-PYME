from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.utils.password import get_current_user
from app.models.user import User
from app.models.pedidos import Pedido, PedidoItems
from app.schemas.pedidos import PedidoCreate, PedidoResponse,PedidoItemCreate, PedidoItemResponse,PedidoUpdate
from app.models.products import Product
from app.models.precios import Precio
from app.models.clientes import Cliente
from datetime import datetime, timezone


router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    for item in pedido.items:
        if db.query(Product).filter(Product.id == item.producto_id).first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        if db.query(Product).filter(Product.id == item.producto_id).first().stock < item.cantidad:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock")
    
    db_pedido = Pedido(
        cliente_id=pedido.cliente_id,
        fecha_pedido=pedido.fecha_pedido,
        estado=pedido.estado,
        metodo_pago=pedido.metodo_pago,
        created_at=pedido.fecha_pedido,
        updated_at=pedido.fecha_pedido
    )
        
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)

    
    cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
    usar_precio_BA = cliente.zona == "Buenos Aires"
    
    if cliente:
        for item in pedido.items:
            precios = db.query(Precio).filter(Precio.productos_id == item.producto_id).order_by(Precio.created_at.desc()).first()
            
            db_item = PedidoItems(
                pedido_id=db_pedido.id,
                producto_id=item.producto_id,
                cantidad=item.cantidad,
                precio_unitario=precios.precio_BA if usar_precio_BA else precios.precio_interior
            )
            db.add(db_item)
            db.query(Product).filter(Product.id == item.producto_id).first().stock -= item.cantidad
        
        db.commit()

    return db_pedido

@router.get("/", response_model=list[PedidoResponse], status_code=status.HTTP_200_OK)
def get_pedidos(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Pedido).all()

@router.get("/{id}", response_model=PedidoResponse, status_code=status.HTTP_200_OK)
def get_pedido(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    return pedido

@router.patch("/{id}", response_model=PedidoResponse, status_code=status.HTTP_200_OK)
def update_pedido(id: int, pedido: PedidoUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_pedido = db.query(Pedido).filter(Pedido.id == id).first()
    if db_pedido is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido not found")
    for key, value in pedido.model_dump(exclude_unset=True).items():
        setattr(db_pedido, key, value)
    db_pedido.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido