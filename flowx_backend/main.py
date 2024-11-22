from fastapi import FastAPI
from flowx_backend.core.event import startup_event, shutdown_event
from flowx_backend.api import  token_router
from contextlib import asynccontextmanager
from flowx_backend.core.config import settings
from flowx_backend.core.cors_config import setup_cors

@asynccontextmanager
async def lifespan(app: FastAPI):
    # connect db
    await startup_event()
    yield
    # disconnect db
    await shutdown_event()


app = FastAPI(lifespan=lifespan)


# app.middleware(JWTAuthMiddleware) #type: ignore
setup_cors(app)


# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)

app.include_router(token_router, prefix=settings.API_VERSION, tags=["token"])


