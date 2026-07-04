from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        from_attributes = True
