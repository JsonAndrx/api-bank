from fastapi import FastAPI
from routers import accounts
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(accounts.router)