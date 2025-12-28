from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    pass

class PatientBase(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: date
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class Patient(PatientBase):
    pass