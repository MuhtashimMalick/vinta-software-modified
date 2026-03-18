import logging
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .schemas import UserCreate, UserRead, UserUpdate
from .users import auth_backend, fastapi_users, AUTH_URL_PATH
from fastapi.middleware.cors import CORSMiddleware
from .utils import simple_generate_unique_route_id
from app.routes.salesorder import router as sales_router
from app.routes.products import router as products_router
from app.routes.customer import router as customer
from app.config import settings
from app.logging_config import setup_logging, log_startup_info, log_shutdown_info
from app.logging_middleware import LoggingMiddleware

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    generate_unique_id_function=simple_generate_unique_route_id,
    openapi_url=settings.OPENAPI_URL,
)

# Add logging middleware (BEFORE CORS to capture all requests)
app.add_middleware(LoggingMiddleware)

# Middleware for CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication and user management routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"/{AUTH_URL_PATH}/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(customer, prefix="/cusotmers",tags=["customers"])
add_pagination(app)


# =====================================================================
# STARTUP AND SHUTDOWN EVENTS
# =====================================================================

@app.on_event("startup")
async def startup_event():
    """Log application startup."""
    log_startup_info()
    logger.info("FastAPI application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown."""
    log_shutdown_info()
    logger.info("FastAPI application shutdown completed")
