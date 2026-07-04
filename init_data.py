import asyncio
from datetime import time
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User
from app.models.room import Room
from app.models.timeslot import TimeSlot
from app.core.security import get_password_hash

async def init_db():
    async with engine.begin() as conn:
        # Если хотите пересоздавать таблицы — раскомментируйте, но осторожно!
        # await conn.run_sync(Base.metadata.drop_all)
        # await conn.run_sync(Base.metadata.create_all)
        pass

    async with AsyncSessionLocal() as session:
        # Проверяем, есть ли уже данные, чтобы не дублировать
        from sqlalchemy import select
        existing_admin = await session.execute(select(User).where(User.email == "admin@example.com"))
        if not existing_admin.scalar_one_or_none():
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_admin=True
            )
            session.add(admin)

        existing_user = await session.execute(select(User).where(User.email == "user@example.com"))
        if not existing_user.scalar_one_or_none():
            user = User(
                email="user@example.com",
                hashed_password=get_password_hash("user123"),
                full_name="John Doe",
                is_admin=False
            )
            session.add(user)

        # Комнаты
        room_a = await session.execute(select(Room).where(Room.name == "Conference A"))
        if not room_a.scalar_one_or_none():
            room_a = Room(name="Conference A", capacity=10, description="Большая комната с проектором")
            session.add(room_a)
        room_b = await session.execute(select(Room).where(Room.name == "Meeting B"))
        if not room_b.scalar_one_or_none():
            room_b = Room(name="Meeting B", capacity=4, description="Маленькая переговорная")
            session.add(room_b)

        await session.flush()

        # Слоты для комнат
        # Сначала получим созданные комнаты
        rooms = await session.execute(select(Room))
        rooms = rooms.scalars().all()
        for room in rooms:
            # Проверяем, есть ли уже слоты
            slots = await session.execute(select(TimeSlot).where(TimeSlot.room_id == room.id))
            if not slots.scalars().first():
                if room.name == "Conference A":
                    slot1 = TimeSlot(room_id=room.id, start_time=time(9,0), end_time=time(11,0))
                    slot2 = TimeSlot(room_id=room.id, start_time=time(13,0), end_time=time(16,0))
                    session.add_all([slot1, slot2])
                elif room.name == "Meeting B":
                    slot1 = TimeSlot(room_id=room.id, start_time=time(10,0), end_time=time(12,0))
                    slot2 = TimeSlot(room_id=room.id, start_time=time(14,0), end_time=time(17,0))
                    session.add_all([slot1, slot2])

        await session.commit()
        print("Initial data inserted.")

if __name__ == "__main__":
    asyncio.run(init_db())
