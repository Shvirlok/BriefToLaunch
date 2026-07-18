from fastapi import APIRouter
from app.api.campaign import router as campaign_router

api_router = APIRouter()
# Include the campaign router (which already has the "/campaign" prefix)
api_router.include_router(campaign_router)
