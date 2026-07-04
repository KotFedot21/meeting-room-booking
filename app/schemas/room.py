from pydantic import BaseModel
from datetime import time
from typing import Optional, List

class TimeSlotBase(BaseModel):
    start_time: time
    end_time: time

class TimeSlotResponse(TimeSlotBase):
    id: int
    room_id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    name: str
    capacity: int
    description: Optional[str] = None

class RoomResponse(RoomBase):
    id: int
    slots: List[TimeSlotResponse] = []

    class Config:
        from_attributes = True
