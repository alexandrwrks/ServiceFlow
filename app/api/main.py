from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.modules.api_v1.router import router as api_v1_router
from app.api.modules.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(_: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_v1_router)
app.include_router(auth_router, tags=["Auth"], prefix="/auth")