from fastapi import FastAPI
from routers import accounts
from dotenv import load_dotenv

load_dotenv()

# Crear instancia de la aplicación FastAPI
app = FastAPI(
    title="API Bank",
    description="API RESTful para gestión de cuentas bancarias",
    version="1.0.0"
)

# Incluir los routers de endpoints
app.include_router(accounts.router)