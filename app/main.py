from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.modules.auth.router import router as auth_router
from app.modules.order.router import router as orders_router
from app.modules.companies.router import router as companies_router

@asynccontextmanager
async def lifespan(_: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router, tags=["Auth"], prefix="/api/v1/auth")
app.include_router(orders_router, tags=["Orders"], prefix="/api/v1/orders")
app.include_router(companies_router, tags=["Companies"], prefix="/api/v1/companies")