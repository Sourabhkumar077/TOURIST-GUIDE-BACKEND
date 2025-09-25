import uuid
from sqlalchemy import Column, String, Date, Integer, ForeignKey, Text, TIMESTAMP, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    user_type = Column(String(20), nullable=False)  # 'tourist' or 'authority'
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    tourist_profile = relationship("TouristProfile", back_populates="user", uselist=False)
    authority_profile = relationship("AuthorityProfile", back_populates="user", uselist=False)


class TouristProfile(Base):
    __tablename__ = "tourist_profiles"
    tourist_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(100), nullable=False)
    document_type = Column(String(50), nullable=False)
    document_number = Column(String(50), nullable=False)
    nationality = Column(String(50))
    trip_start = Column(Date)
    trip_end = Column(Date)
    emergency_contact_name = Column(String(100))
    emergency_contact_phone = Column(String(20))
    blockchain_id = Column(String(255))
    qr_code_url = Column(Text)
    safety_score = Column(Integer, default=100)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="tourist_profile")


class AuthorityProfile(Base):
    __tablename__ = "authority_profiles"
    authority_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    designation = Column(String(100))
    contact_number = Column(String(20))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="authority_profile")


class Incident(Base):
    __tablename__ = "incidents"
    incident_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tourist_id = Column(UUID(as_uuid=True), ForeignKey("tourist_profiles.tourist_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # 'Theft', 'Harassment', 'Medical', 'Accident'
    latitude = Column(String(50))
    longitude = Column(String(50))
    status = Column(String(20), default="Active")  # 'Active', 'Resolved'
    priority = Column(String(20), default="Medium")  # 'Low', 'Medium', 'High', 'Critical'
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    tourist = relationship("TouristProfile", backref="incidents")


class Alert(Base):
    __tablename__ = "alerts"
    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    incident_id = Column(UUID(as_uuid=True), ForeignKey("incidents.incident_id", ondelete="CASCADE"), nullable=False)
    tourist_id = Column(UUID(as_uuid=True), ForeignKey("tourist_profiles.tourist_id", ondelete="CASCADE"), nullable=False)
    distance_km = Column(String(20))
    is_read = Column(String(10), default="false")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    incident = relationship("Incident", backref="alerts")
    tourist = relationship("TouristProfile", backref="alerts")