from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
import uuid

from ..database import get_db
from ..models import User, TouristProfile, AuthorityProfile
from ..schemas import TouristRegister, AuthorityRegister, UserLogin

router = APIRouter()

# ----------------------
# Tourist Register  (working)
# ----------------------
@router.post("/register/tourist") 
def register_tourist(data: TouristRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(email=data.email, password_hash=bcrypt.hash(data.password), user_type="tourist")
    db.add(new_user)
    db.flush()

    tourist_profile = TouristProfile(
        tourist_id=new_user.user_id,
        full_name=data.full_name,
        document_type=data.document_type,
        document_number=data.document_number[-4:],  # last 4 digits
        nationality=data.nationality,
        trip_start=data.trip_start,
        trip_end=data.trip_end,
        emergency_contact_name=data.emergency_contact_name,
        emergency_contact_phone=data.emergency_contact_phone,
        blockchain_id=str(uuid.uuid4())
    )
    db.add(tourist_profile)
    db.commit()
    db.refresh(new_user)

    return {"message": "Tourist registered", "user_id": str(new_user.user_id)}

# ----------------------
# Authority Register   (working)
# ----------------------
@router.post("/register/authority")
def register_authority(data: AuthorityRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(email=data.email, password_hash=bcrypt.hash(data.password), user_type="authority")
    db.add(new_user)
    db.flush()

    authority_profile = AuthorityProfile(
        authority_id=new_user.user_id,
        full_name=data.full_name,
        department=data.department,
        designation=data.designation if data.designation else None,
        contact_number=data.contact_number if data.contact_number else None
    )
    db.add(authority_profile)
    db.commit()
    db.refresh(new_user)

    return {"message": "Authority registered", "user_id": str(new_user.user_id)}

# ----------------------
# Login (both)  (working)
# ----------------------
@router.post("/login")
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not bcrypt.verify(data.password, str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    result = {"user_id": str(user.user_id), "user_type": user.user_type}

    if str(user.user_type) == "tourist":
        profile = db.query(TouristProfile).filter_by(tourist_id=user.user_id).first()
        if profile:
            result.update({
                "full_name": profile.full_name,
                "blockchain_id": profile.blockchain_id
            })
    else:
        profile = db.query(AuthorityProfile).filter_by(authority_id=user.user_id).first()
        if profile:
            result.update({
                "full_name": profile.full_name,
                "department": profile.department
            })

    return {"message": "Login successful", "user": result}
