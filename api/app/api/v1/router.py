"""
API v1 router configuration.
Aggregates all v1 endpoints and organizes them by feature.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, info

# Create the main API router
api_router = APIRouter()

# Include health check endpoints
api_router.include_router(
    health.router,
    prefix="",  # No additional prefix for health endpoints
    tags=["Health"],
)

# Include application info endpoint
api_router.include_router(
    info.router,
    prefix="",  # No additional prefix for info endpoint
    tags=["Information"],
)

# Future endpoints will be added here:
# api_router.include_router(
#     auth.router,
#     prefix="/auth",
#     tags=["Authentication"]
# )
#
# api_router.include_router(
#     users.router,
#     prefix="/users",
#     tags=["Users"]
# )
#
# api_router.include_router(
#     chat.router,
#     prefix="/chat",
#     tags=["Chat"]
# )
