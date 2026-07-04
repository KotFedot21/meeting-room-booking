from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.room import Room
from app.models.timeslot import TimeSlot
from app.schemas.room import RoomResponse, RoomCreate

router = APIRouter()

@router.get("/", response_model=list[RoomResponse])
async def get_rooms(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить список всех комнат с их слотами"""
    result = await db.execute(select(Room))
    rooms = result.scalars().all()
    # Подгружаем слоты для каждой комнаты (можно через joinedload)
    for room in rooms:
        slots_result = await db.execute(select(TimeSlot).where(TimeSlot.room_id == room.id))
        room.slots = slots_result.scalars().all()
    return rooms

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить комнату по ID с её слотами"""
    room = await db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    slots_result = await db.execute(select(TimeSlot).where(TimeSlot.room_id == room.id))
    room.slots = slots_result.scalars().all()
    return room
