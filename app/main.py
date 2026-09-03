
from contextlib import asynccontextmanager
import time
import uuid

import joblib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.logging_config import setup_logging
from app.exceptions import InvalidInputShapeError
from app.routers.v1 import router as v1_router
from app.routers.v2 import router as v2_router


logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading ML model...")

    app.state.model = joblib.load(settings.MODEL_PATH)
    app.state.logger = logger

    logger.info("ML model loaded successfully!")

    yield


app = FastAPI(
    title=settings.API_TITLE,
    lifespan=lifespan
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = (time.time() - start_time) * 1000

    logger.info(
        "request_id=%s method=%s path=%s status=%s duration=%.2fms",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration
    )

    response.headers["X-Request-ID"] = request_id

    return response


@app.exception_handler(InvalidInputShapeError)
async def invalid_input_shape_handler(
    request: Request,
    exc: InvalidInputShapeError
):
    logger.warning(
        "request_id=%s Invalid input shape",
        request.state.request_id
    )

    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid input shape"}
    )


@app.get("/")
def root():
    return {"message": "ML API is alive"}


app.include_router(v1_router)
app.include_router(v2_router)

