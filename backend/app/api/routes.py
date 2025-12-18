from fastapi import APIRouter
from app.api.notes import router as notes
from app.api.rs import router as recommendations
from app.api.profile import router as profile
from app.api.admin_routers import router as admin

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}