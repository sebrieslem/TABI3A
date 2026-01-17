from pydantic import BaseModel, EmailStr
from typing import Optional, List


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ParkBase(BaseModel):
    name: str
    description: Optional[str] = None
    rules: Optional[str] = None
    best_seasons: Optional[str] = None


class ParkCreate(ParkBase):
    pass


class ParkResponse(ParkBase):
    id: int

    class Config:
        from_attributes = True

class RoleUpdate(BaseModel):
    role: str

class SpeciesBase(BaseModel):
    common_name: str
    scientific_name: str | None = None
    category: str  # FAUNA / FLORA
    conservation_status: str | None = None
    endemic: bool = False


class SpeciesCreate(SpeciesBase):
    park_ids: List[int] = []


class SpeciesResponse(SpeciesBase):
    id: int

    class Config:
        from_attributes = True

class ParkUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    rules: str | None = None
    best_seasons: str | None = None

class SpeciesUpdate(BaseModel):
    conservation_status: str | None = None
    endemic: bool | None = None
