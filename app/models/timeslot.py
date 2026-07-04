from sqlalchemy import Time, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class TimeSlot(Base):
    __tablename__ = "timeslots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    start_time: Mapped[str] = mapped_column(Time, nullable=False)
    end_time: Mapped[str] = mapped_column(Time, nullable=False)

    room = relationship("Room", back_populates="slots")
