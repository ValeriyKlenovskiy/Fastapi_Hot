import asyncio
from contextlib import asynccontextmanager
import sentry_sdk
import time


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI, version
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as rooms_router
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.importer.router import router as importer_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.prometheus.router import router as prometheus_router
from app.users.router import router as users_router


sentry_sdk.init(
    dsn="https://3fc2e17e955179e3339aebd06dcddc1e@o4506687619727360.ingest.sentry.io/4506687622545408",
    traces_sample_rate=1.0,
)


async def get_cache():
    while True:
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    # asyncio.create_task(get_cache())
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(bookings_router)
app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(pages_router)
app.include_router(images_router)
app.include_router(importer_router)
app.include_router(prometheus_router)

app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # При подключении Prometheus + Grafana подобный лог не требуется
    logger.info("Request handling time", extra={
        "process_time": round(process_time, 4)
    })
    return response


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}',)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)

Instrumentator().instrument(app).expose(app)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
