import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings

def get_password_hash(password: str) -> str:
    """Возвращает хеш пароля"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли пароль хешу"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Создаёт JWT токен"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    """Декодирует JWT токен"""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
