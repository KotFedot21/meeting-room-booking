from sqlalchemy import Date, Time, ForeignKey, Enum, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, time, datetime
import enum
from app.core.database import Base

class BookingStatus(str, enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.ACTIVE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    room = relationship("Room", back_populates="bookings")
    user = relationship("User", back_populates="bookings")
