from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


# ----------------------
# Tourist
# ----------------------
class TouristRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    document_type: str
    document_number: str
    nationality: str
    trip_start: date
    trip_end: date
    emergency_contact_name: str
    emergency_contact_phone: str

# ----------------------
# Authority
# ----------------------
class AuthorityRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    department: str
    designation: Optional[str]
    contact_number: Optional[str]

# ----------------------
# Login
# ----------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str
