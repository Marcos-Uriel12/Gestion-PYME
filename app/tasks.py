import smtplib
from email.mime.text import MIMEText
from app.celery_app import celery_app
from dotenv import load_dotenv
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
from app.models.pedidos import Pedido, PedidoItems
from app.database.database import SessionLocal
from app.models.clientes import Cliente




load_dotenv()

@celery_app.task
def enviar_email_pedido(email: str, pedido_id: int, producto_id: int, cantidad: int, 
    precio_unitario: float, estado: str, fecha_pedido: datetime):

    msg = MIMEMultipart()
    msg['Subject'] = 'Confirmación de pedido'
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = email

    body = MIMEText(f"""
    Tu pedido #{pedido_id} fue recibido correctamente.

    Detalles del pedido:
    Producto: {producto_id}
    Cantidad: {cantidad}
    Precio unitario: {precio_unitario}
    Estado: {estado}
    Fecha del pedido: {fecha_pedido}
    Total: {cantidad * precio_unitario}
    Gracias por tu compra.
    """)

    msg.attach(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)

@celery_app.task
def update_pedido(pedido_id: int, estado: str):
    #Obtener email:
    db = SessionLocal()
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    cliente = db.query(Cliente).filter(Cliente.id == pedido.cliente_id).first()
    email = cliente.email
    db.close()

    msg = MIMEMultipart()
    msg['Subject'] = 'Actualización de pedido'
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = email

    body = MIMEText(f"""
    Tu pedido #{pedido_id} fue actualizado correctamente.

    Detalles del pedido:
    Estado: {estado}
    Fecha del pedido: {datetime.now(timezone.utc)}
    """)

    msg.attach(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
