# API REST - Gestión PYME

API REST para la gestión integral de una pequeña o mediana empresa (PYME) orientada a la venta de productos (muebles u otros artículos con medidas y unidades de medida). El sistema centraliza todas las operaciones del negocio en un solo backend:

- **Catálogo de productos**: cada producto tiene nombre, stock, unidad de medida, medidas opcionales, tipo de mueble y categoría. El stock se descuenta automáticamente al confirmar un pedido.

- **Gestión de clientes**: los clientes se registran con datos de contacto (email, teléfono, dirección, ciudad, código postal) y se clasifican por zona geográfica (**Buenos Aires** o **Interior**), lo que determina qué precio se les aplica en cada pedido.

- **Precios duales por zona**: cada producto tiene dos precios vigentes almacenados históricamente — `precio_BA` para clientes de Buenos Aires y `precio_interior` para el resto del país. El sistema siempre toma el precio más reciente al momento de crear el pedido.

- **Pedidos con ítems múltiples**: un pedido puede contener varios productos a la vez. Cada ítem registra la cantidad y el precio unitario aplicado según la zona del cliente. El pedido pasa por estados (`pendiente → en_proceso → enviado → entregado / cancelado`) y registra el método de pago.

- **Autenticación con JWT**: todos los endpoints de negocio están protegidos. Un usuario debe registrarse y hacer login para obtener un token de acceso con expiración de 30 minutos.

- **Historial y auditoría**: todos los modelos registran `created_at` y `updated_at` para trazabilidad completa de cambios.

## Stack

- **FastAPI** — framework web
- **PostgreSQL** — base de datos
- **SQLAlchemy 2.0** — ORM
- **Alembic** — migraciones
- **JWT (jose)** — autenticación
- **Docker Compose** — base de datos local
- **Python 3.13**

## Módulos

| Prefijo | Descripción |
|---|---|
| `/auth` | Registro y login de usuarios |
| `/categorias` | CRUD de categorías de productos |
| `/productos` | CRUD de productos con stock |
| `/clientes` | CRUD de clientes |
| `/precios` | Precios por producto (BA vs Interior) |
| `/pedidos` | Pedidos con descuento automático de stock |

## Instalación

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

### 3. Configurar variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql+psycopg2://marcos:marcos123@localhost:5432/pyme_db
SECRET_KEY=unaclavesecretamuylargarandom123456
```

> Cambiar `SECRET_KEY` por un valor seguro en producción.

### 4. Levantar la base de datos con Docker

```bash
docker-compose up -d
```

Esto levanta un contenedor PostgreSQL en el puerto `5432`.

### 5. Ejecutar migraciones

```bash
alembic upgrade head
```

### 6. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`.

Documentación interactiva: `http://localhost:8000/docs`

## Autenticación

Los endpoints protegidos requieren un token JWT tipo Bearer.

1. Registrar usuario: `POST /auth/register`
2. Obtener token: `POST /auth/login` (con `username` y `password` en form-data)
3. Incluir en el header: `Authorization: Bearer <token>`

## Estructura del proyecto

```
proyecto_taller/
├── app/
│   ├── main.py
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

## Lógica de precios

Al crear un pedido, el precio unitario se asigna automáticamente según la zona del cliente:
- **Buenos Aires** → `precio_BA`
- **Interior** → `precio_interior`
