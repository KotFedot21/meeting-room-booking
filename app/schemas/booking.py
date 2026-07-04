from pydantic import BaseModel, validator
from datetime import date, time
from typing import Optional
from enum import Enum

class BookingStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"

class BookingBase(BaseModel):
    room_id: int
    date: date
    start_time: time
    end_time: time

    @validator('end_time')
    def end_after_start(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    status: BookingStatus

    class Config:
        from_attributes = True
