# API REST — Gestión PYME

API REST para la gestión integral de una PYME orientada a la venta de productos, con catálogo, clientes, pedidos, precios duales por zona y notificaciones por email.

## Demo

🚀 Ver demo en Railway: https://gestion-pyme-production-849b.up.railway.app/docs

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-migrations-6BA81E?style=flat)
![Celery](https://img.shields.io/badge/Celery-5.x-37814A?style=flat&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-broker-DC382D?style=flat&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-auth-000000?style=flat&logo=jsonwebtokens&logoColor=white)

---

## Features

- **Autenticación JWT** — registro y login con tokens Bearer de 30 min de expiración.
- **Catálogo de productos** — CRUD con stock, unidad de medida, medidas opcionales y categoría. El stock se descuenta automáticamente al confirmar un pedido.
- **Gestión de clientes** — datos de contacto completos y clasificación por zona geográfica (Buenos Aires / Interior).
- **Pedidos con ítems múltiples** — cada pedido agrupa varios productos y fluye por estados: `pendiente → en_proceso → enviado → entregado / cancelado`.
- **Precios duales con historial** — cada producto tiene `precio_BA` y `precio_interior`. El sistema aplica el precio vigente al momento de crear el pedido y conserva el historial completo.
- **Notificaciones por email con Celery** — al crear un pedido o cambiar su estado, se envía un email automático al cliente de forma asíncrona via Redis + Celery.

---

## Levantar localmente

### Requisitos

- Python 3.13
- Docker y Docker Compose
- Redis (levantado con Docker, ver más abajo)

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd proyecto_taller
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Variables de entorno

Crear un archivo `.env` en la raíz:

```env
DATABASE_URL=postgresql+psycopg2://marcos:marcos123@localhost:5432/pyme_db
SECRET_KEY=unaclavesecretamuylargarandom123456
REDIS_URL=redis://localhost:6379/0
EMAIL=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password
```

> Para `EMAIL_PASSWORD` usá una App Password de Google (no tu contraseña real).

### 4. Levantar servicios con Docker Compose

```bash
docker-compose up -d
```

Levanta PostgreSQL en el puerto `5432` y Redis en el `6379`.

### 5. Ejecutar migraciones

```bash
alembic upgrade head
```

### 6. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

API disponible en `http://localhost:8000`  
Docs interactivos: `http://localhost:8000/docs`

### 7. Iniciar el worker de Celery

En una terminal separada (con el venv activado):

```bash
celery -A app.celery_app worker --loglevel=info
```

---

## Estructura de carpetas

```text
proyecto_taller/
├── app/
│   ├── main.py
│   ├── celery_app.py
│   ├── tasks.py
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── categoria.py
│   │   ├── products.py
│   │   ├── clientes.py
│   │   ├── precios.py
│   │   └── pedidos.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── categoria.py
│   │   ├── productos.py
│   │   ├── cliente.py
│   │   ├── precios.py
│   │   └── pedidos.py
│   ├── schemas/
│   └── utils/
│       └── password.py
├── alembic/
├── docker-compose.yml
├── requirements.txt
└── .env
```
