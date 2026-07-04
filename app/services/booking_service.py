from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, time

from app.models.booking import Booking, BookingStatus
from app.models.timeslot import TimeSlot

async def check_room_availability(
    db: AsyncSession,
    room_id: int,
    booking_date: date,
    start_time: time,
    end_time: time,
    exclude_booking_id: int | None = None
) -> bool:
    """
    Проверяет, свободна ли комната в указанный интервал времени.
    Возвращает True, если свободна, False — если занята.
    """
    query = select(Booking).where(
        and_(
            Booking.room_id == room_id,
            Booking.date == booking_date,
            Booking.status == BookingStatus.ACTIVE,
            Booking.start_time < end_time,
            Booking.end_time > start_time
        )
    )
    if exclude_booking_id:
        query = query.where(Booking.id != exclude_booking_id)
    
    result = await db.execute(query)
    return result.scalar_one_or_none() is None

async def is_time_within_slot(
    db: AsyncSession,
    room_id: int,
    start_time: time,
    end_time: time
) -> bool:
    """
    Проверяет, что указанный интервал полностью лежит внутри одного из слотов комнаты.
    """
    result = await db.execute(
        select(TimeSlot).where(
            and_(
                TimeSlot.room_id == room_id,
                TimeSlot.start_time <= start_time,
                TimeSlot.end_time >= end_time
            )
        )
    )
    return result.scalar_one_or_none() is not None
