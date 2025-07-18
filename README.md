# API Bank

Una API RESTful para gestión de cuentas bancarias construida con FastAPI y MongoDB, siguiendo una arquitectura en capas limpia y separación de responsabilidades.

## 📋 Descripción

Esta API permite realizar operaciones básicas de gestión de cuentas bancarias:
- **Crear cuentas**: Registrar nuevas cuentas con información del titular
- **Consultar cuentas**: Obtener listado de todas las cuentas registradas
- **Actualizar saldo**: Modificar el balance de una cuenta específica

## 🏗️ Arquitectura

El proyecto implementa una **arquitectura en capas** que garantiza la separación de responsabilidades y facilita el mantenimiento:

```
src/
├── main.py                 # Punto de entrada de la aplicación
├── database.py             # Configuración de conexión a MongoDB
├── models/                 # Capa de Modelos (Pydantic)
│   └── account_model.py    
├── repositories/           # Capa de Acceso a Datos
│   └── account_repository.py
├── services/               # Capa de Lógica de Negocio
│   └── account_service.py
├── routers/                # Capa de Presentación (FastAPI)
│   └── accounts.py
└── tests/                  # Pruebas unitarias
    └── test_accounts.py
```

### Capas de la Arquitectura

- **🔧 Modelos**: Definen la estructura de datos usando Pydantic para validación automática
- **💾 Repositorios**: Manejan la persistencia de datos y operaciones con MongoDB
- **🔄 Servicios**: Contienen la lógica de negocio y reglas de validación
- **🌐 Routers**: Exponen los endpoints HTTP y manejan las peticiones/respuestas

## 🚀 Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para Python
- **MongoDB**: Base de datos NoSQL para persistencia
- **Pydantic**: Validación de datos y serialización
- **Docker**: Containerización de la aplicación
- **Pytest**: Framework de testing

## 📋 Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.12+ (si se ejecuta localmente)

## 🛠️ Instalación y Ejecución

### Con Docker (Recomendado)

1. **Clonar el repositorio**:
```bash
git clone https://github.com/JsonAndrx/api-bank.git
cd api-bank
```

2. **Crear archivo de variables de entorno**:
```bash
# Crear archivo .env
echo "MONGO_URI=mongodb://root:root@mongo:27017/api_bank?authSource=admin" > .env
```

3. **Levantar la aplicación**:
```bash
docker-compose up --build
```

La API estará disponible en: `http://localhost:8000`

### Ejecución Local

1. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

2. **Configurar variables de entorno**:
```bash
# .env
MONGO_URI=mongodb://root:root@localhost:27017/api_bank?authSource=admin
```

3. **Ejecutar MongoDB con Docker**:
```bash
docker run -d -p 27017:27017 --name mongo \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=root \
  mongo
```

4. **Ejecutar la aplicación**:
```bash
cd src
fastapi run main.py --reload --port 8000
```

## 📖 Endpoints de la API

### Documentación Interactiva
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/accounts` | Crear una nueva cuenta |
| GET | `/accounts` | Obtener todas las cuentas |
| PATCH | `/accounts/{account_number}` | Actualizar saldo de una cuenta |

### 💡 Ejemplos de Uso

**Crear cuenta**:
```bash
curl -X POST "http://localhost:8000/accounts" \
  -H "Content-Type: application/json" \
  -d '{
    "account_number": "123456789",
    "holder_name": "John Doe",
    "account_type": "saving",
    "balance": 1000.0,
    "currency": "USD"
  }'
```

**Obtener todas las cuentas**:
```bash
curl -X GET "http://localhost:8000/accounts"
```

**Actualizar saldo**:
```bash
curl -X PATCH "http://localhost:8000/accounts/123456789" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "account_id_here",
    "balance": 500.0
  }'
```

## 🧪 Testing

Ejecutar las pruebas unitarias:

```bash
# Con Docker
docker-compose exec app pytest tests/

# Localmente
cd src
pytest tests/
```

Las pruebas incluyen:
- ✅ Creación exitosa de cuentas
- ❌ Manejo de cuentas duplicadas
- 🔄 Actualización de saldos
- 🗂️ Consulta de cuentas
- 💥 Manejo de errores de base de datos

## 📊 Estructura de Datos

### Tipos de Cuenta
- `saving`: Cuenta de ahorro
- `checking`: Cuenta corriente

### Monedas Soportadas
- `USD`: Dólar estadounidense
- `EUR`: Euro

### Validaciones
- Número de cuenta: 5-20 caracteres
- Nombre del titular: Máximo 100 caracteres
- Saldo: Debe ser mayor o igual a 1

## 🔧 Variables de Entorno

```env
MONGO_URI=mongodb://admin:admin@mongo:27017/api_bank?authSource=admin
```

## 👨‍💻 Autor

**JsonAndrx** - [GitHub](https://github.com/JsonAndrx)

---
