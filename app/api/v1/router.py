from fastapi import APIRouter
from app.api.v1.endpoints import auth, rooms, bookings

router = APIRouter(prefix="/api/v1")

router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
