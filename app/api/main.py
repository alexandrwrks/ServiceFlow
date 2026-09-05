from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.modules.api_v1.router import router as api_v1_router

@asynccontextmanager
async def lifespan(_: FastAPI):

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(api_v1_router)