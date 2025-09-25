from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional
from uuid import UUID


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

# ----------------------
# Incident
# ----------------------
class IncidentCreate(BaseModel):
    title: str
    description: str
    category: str
    latitude: Optional[str] = None
    longitude: Optional[str] = None

class IncidentResponse(BaseModel):
    incident_id: str
    title: str
    description: str
    category: str
    latitude: Optional[str]
    longitude: Optional[str]
    status: str
    priority: str
    created_at: datetime
    distance: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------------
# Alert
# ----------------------
class AlertResponse(BaseModel):
    alert_id: str
    incident_id: str
    title: str
    category: str
    distance: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ----------------------
# User Response
# ----------------------
class UserResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    user_type: str
    blockchain_id: Optional[str] = None
    department: Optional[str] = None

    class Config:
        from_attributes = True
