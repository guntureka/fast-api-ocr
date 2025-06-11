from fastapi import APIRouter

from app.api.routes import energy_expert

api_router = APIRouter()
api_router.include_router(energy_expert.router)
