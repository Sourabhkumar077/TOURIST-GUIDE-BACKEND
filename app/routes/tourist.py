from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import math

from ..database import get_db
from ..models import TouristProfile, Incident, Alert, User
from ..schemas import IncidentCreate, IncidentResponse, AlertResponse

router = APIRouter()

# ----------------------
# Get Tourist Profile
# ----------------------
@router.get("/profile/{user_id}")
def get_tourist_profile(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(TouristProfile).filter(TouristProfile.tourist_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Tourist profile not found")
    
    return {
        "tourist_id": str(profile.tourist_id),
        "full_name": profile.full_name,
        "document_type": profile.document_type,
        "document_number": profile.document_number,
        "nationality": profile.nationality,
        "trip_start": profile.trip_start,
        "trip_end": profile.trip_end,
        "emergency_contact_name": profile.emergency_contact_name,
        "emergency_contact_phone": profile.emergency_contact_phone,
        "blockchain_id": profile.blockchain_id,
        "safety_score": profile.safety_score
    }

# ----------------------
# Create Incident
# ----------------------
@router.post("/incidents", response_model=IncidentResponse)
def create_incident(incident_data: IncidentCreate, tourist_id: str, db: Session = Depends(get_db)):
    # Verify tourist exists
    tourist = db.query(TouristProfile).filter(TouristProfile.tourist_id == tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist not found")
    
    # Create incident
    incident = Incident(
        tourist_id=tourist_id,
        title=incident_data.title,
        description=incident_data.description,
        category=incident_data.category,
        latitude=incident_data.latitude,
        longitude=incident_data.longitude
    )
    
    db.add(incident)
    db.commit()
    db.refresh(incident)
    
    return IncidentResponse(
        incident_id=str(incident.incident_id),
        title=incident.title,
        description=incident.description,
        category=incident.category,
        latitude=incident.latitude,
        longitude=incident.longitude,
        status=incident.status,
        priority=incident.priority,
        created_at=incident.created_at
    )

# ----------------------
# Get Tourist's Incidents
# ----------------------
@router.get("/incidents/{tourist_id}", response_model=List[IncidentResponse])
def get_tourist_incidents(tourist_id: str, db: Session = Depends(get_db)):
    incidents = db.query(Incident).filter(Incident.tourist_id == tourist_id).all()
    
    return [
        IncidentResponse(
            incident_id=str(incident.incident_id),
            title=incident.title,
            description=incident.description,
            category=incident.category,
            latitude=incident.latitude,
            longitude=incident.longitude,
            status=incident.status,
            priority=incident.priority,
            created_at=incident.created_at
        ) for incident in incidents
    ]

# ----------------------
# Get Nearby Alerts
# ----------------------
@router.get("/alerts/{tourist_id}", response_model=List[AlertResponse])
def get_tourist_alerts(tourist_id: str, db: Session = Depends(get_db)):
    # Get all alerts for this tourist
    alerts = db.query(Alert).filter(Alert.tourist_id == tourist_id).all()
    
    result = []
    for alert in alerts:
        incident = db.query(Incident).filter(Incident.incident_id == alert.incident_id).first()
        if incident:
            result.append(AlertResponse(
                alert_id=str(alert.alert_id),
                incident_id=str(alert.incident_id),
                title=incident.title,
                category=incident.category,
                distance=alert.distance_km,
                status=incident.status,
                created_at=alert.created_at
            ))
    
    return result

# ----------------------
# Create Alert for Nearby Tourists
# ----------------------
@router.post("/alerts/create")
def create_alert_for_nearby_tourists(incident_id: str, db: Session = Depends(get_db)):
    # Get the incident
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Get all tourists (in a real app, you'd filter by location)
    tourists = db.query(TouristProfile).all()
    
    alerts_created = 0
    for tourist in tourists:
        # Skip the tourist who created the incident
        if str(tourist.tourist_id) == str(incident.tourist_id):
            continue
            
        # Calculate distance (simplified - in real app use proper geolocation)
        distance = "2.5km"  # Placeholder
        
        # Create alert
        alert = Alert(
            incident_id=incident_id,
            tourist_id=tourist.tourist_id,
            distance_km=distance
        )
        db.add(alert)
        alerts_created += 1
    
    db.commit()
    return {"message": f"Created {alerts_created} alerts for nearby tourists"}

# ----------------------
# Update Safety Score
# ----------------------
@router.put("/safety-score/{tourist_id}")
def update_safety_score(tourist_id: str, score: int, db: Session = Depends(get_db)):
    tourist = db.query(TouristProfile).filter(TouristProfile.tourist_id == tourist_id).first()
    if not tourist:
        raise HTTPException(status_code=404, detail="Tourist not found")
    
    tourist.safety_score = max(0, min(100, score))  # Clamp between 0-100
    db.commit()
    
    return {"message": "Safety score updated", "new_score": tourist.safety_score}
