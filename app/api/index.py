from fastapi import APIRouter

from app.api.routes import energy_expert

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(energy_expert.router)
