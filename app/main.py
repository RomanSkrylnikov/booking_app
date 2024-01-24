from contextlib import asynccontextmanager
from datetime import date
import time
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import logger
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.logger import logger
from app.users.router import router as router_users
from app.prometheus.router import router as router_prometheus


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin.*', '/metricks'],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

app.mount('/static', StaticFiles(directory='app/static'), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_prometheus)

origins = [
    'http://localhost:3000'
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATH', 'PUT'],
                   allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                                  'Access-Control=Allow-Origin', 'Authorization'],
                   )


@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info('Request handling time', extra={
        'process_time': round(process_time, 4)
    })
    return response


