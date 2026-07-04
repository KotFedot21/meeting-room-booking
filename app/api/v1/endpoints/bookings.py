from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, time
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.models.booking import Booking, BookingStatus
from app.models.room import Room
from app.models.timeslot import TimeSlot
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import check_availability

router = APIRouter()

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking_data: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Проверка существования комнаты
    room = await db.get(Room, booking_data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")

    # Проверка, что время попадает в слоты комнаты
    slots_result = await db.execute(
        select(TimeSlot).where(
            and_(
                TimeSlot.room_id == booking_data.room_id,
                TimeSlot.start_time <= booking_data.start_time,
                TimeSlot.end_time >= booking_data.end_time
            )
        )
    )
    if not slots_result.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Time interval does not fit any allowed slot for this room"
        )

    # Проверка на конфликт
    if not await check_availability(
        db,
        booking_data.room_id,
        booking_data.date,
        booking_data.start_time,
        booking_data.end_time
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Room is already booked for this time"
        )

    # Создание бронирования
    new_booking = Booking(
        room_id=booking_data.room_id,
        user_id=current_user.id,
        date=booking_data.date,
        start_time=booking_data.start_time,
        end_time=booking_data.end_time,
        status=BookingStatus.ACTIVE
    )
    db.add(new_booking)
    await db.commit()
    await db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=list[BookingResponse])
async def get_my_bookings(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Получить все бронирования текущего пользователя"""
    result = await db.execute(
        select(Booking)
        .where(Booking.user_id == current_user.id)
        .order_by(Booking.date, Booking.start_time)
    )
    return result.scalars().all()

@router.delete("/{booking_id}")
async def cancel_booking(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Отменить бронирование (только владелец или админ)"""
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Проверка прав
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this booking"
        )
    
    booking.status = BookingStatus.CANCELLED
    await db.commit()
    return {"message": "Booking cancelled"}

# Админский эндпоинт для просмотра всех бронирований
@router.get("/admin/all", response_model=list[BookingResponse])
async def get_all_bookings(
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
):
    """Получить все бронирования (только для админов)"""
    result = await db.execute(
        select(Booking).order_by(Booking.date, Booking.start_time)
    )
    return result.scalars().all()
