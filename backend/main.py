from contextlib import asynccontextmanager

import aio_pika
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from modules.auth.router import router as auth_router
from modules.order.router import router as orders_router
from modules.companies.router import router as companies_router
from modules.employees.router import router as employees_router
from modules.services.router import router as services_router
from modules.health.router   import router as health_router
from modules.personal.router import router as personal_router
from modules.telegram.router import router as telegram_router
from utils.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = await aio_pika.connect_robust(settings.RabbitMQ_URL)
    
    app.state.rabbitmq_conn = conn

    yield

    await conn.close()


app = FastAPI(lifespan=lifespan)

Instrumentator(
    excluded_handlers=["/metrics", "/docs"],
).instrument(app).expose(app, endpoint="/metrics")

app.include_router(auth_router, tags=["Auth"], prefix="/api/v1/auth")
app.include_router(orders_router, tags=["Orders"], prefix="/api/v1/orders")
app.include_router(companies_router, tags=["Companies"], prefix="/api/v1/companies")
app.include_router(employees_router,  prefix="/api/v1")
app.include_router(services_router, tags=["Services"], prefix="/api/v1/services")
app.include_router(health_router, tags=["Health"])
app.include_router(personal_router, tags=["Personal"], prefix="/api/v1/personal")
app.include_router(telegram_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:63342",
        "http://localhost:63342",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)