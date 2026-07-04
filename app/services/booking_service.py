from typing import Optional 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import date, time
from app.models.booking import Booking, BookingStatus

async def check_availability(
    db: AsyncSession,
    room_id: int,
    booking_date: date,
    start_time: time,
    end_time: time,
    exclude_booking_id: Optional[int] = None
) -> bool:
    """Проверяет, свободна ли комната в указанный интервал"""
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
