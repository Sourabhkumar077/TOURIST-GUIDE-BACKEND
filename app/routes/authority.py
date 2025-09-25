from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from ..models import AuthorityProfile, Incident, Alert, TouristProfile
from ..schemas import IncidentResponse, AlertResponse

router = APIRouter()

# ----------------------
# Get Authority Profile
# ----------------------
@router.get("/profile/{user_id}")
def get_authority_profile(user_id: str, db: Session = Depends(get_db)):
    profile = db.query(AuthorityProfile).filter(AuthorityProfile.authority_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Authority profile not found")
    
    return {
        "authority_id": str(profile.authority_id),
        "full_name": profile.full_name,
        "department": profile.department,
        "designation": profile.designation,
        "contact_number": profile.contact_number
    }

# ----------------------
# Get All Incidents
# ----------------------
@router.get("/incidents", response_model=List[IncidentResponse])
def get_all_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.created_at.desc()).all()
    
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
# Get Incidents by Status
# ----------------------
@router.get("/incidents/status/{status}", response_model=List[IncidentResponse])
def get_incidents_by_status(status: str, db: Session = Depends(get_db)):
    incidents = db.query(Incident).filter(Incident.status == status).order_by(Incident.created_at.desc()).all()
    
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
# Update Incident Status
# ----------------------
@router.put("/incidents/{incident_id}/status")
def update_incident_status(incident_id: str, new_status: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    if new_status not in ["Active", "Resolved"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'Active' or 'Resolved'")
    
    incident.status = new_status
    incident.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Incident status updated to {new_status}"}

# ----------------------
# Update Incident Priority
# ----------------------
@router.put("/incidents/{incident_id}/priority")
def update_incident_priority(incident_id: str, priority: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    if priority not in ["Low", "Medium", "High", "Critical"]:
        raise HTTPException(status_code=400, detail="Invalid priority. Must be 'Low', 'Medium', 'High', or 'Critical'")
    
    incident.priority = priority
    incident.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": f"Incident priority updated to {priority}"}

# ----------------------
# Get All Alerts
# ----------------------
@router.get("/alerts", response_model=List[AlertResponse])
def get_all_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).all()
    
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
# Get Tourist Statistics
# ----------------------
@router.get("/statistics/tourists")
def get_tourist_statistics(db: Session = Depends(get_db)):
    total_tourists = db.query(TouristProfile).count()
    active_incidents = db.query(Incident).filter(Incident.status == "Active").count()
    resolved_incidents = db.query(Incident).filter(Incident.status == "Resolved").count()
    
    return {
        "total_tourists": total_tourists,
        "active_incidents": active_incidents,
        "resolved_incidents": resolved_incidents,
        "total_incidents": active_incidents + resolved_incidents
    }

# ----------------------
# Get Incident Details
# ----------------------
@router.get("/incidents/{incident_id}/details")
def get_incident_details(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    tourist = db.query(TouristProfile).filter(TouristProfile.tourist_id == incident.tourist_id).first()
    
    return {
        "incident": {
            "incident_id": str(incident.incident_id),
            "title": incident.title,
            "description": incident.description,
            "category": incident.category,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "status": incident.status,
            "priority": incident.priority,
            "created_at": incident.created_at,
            "updated_at": incident.updated_at
        },
        "tourist": {
            "tourist_id": str(tourist.tourist_id) if tourist else None,
            "full_name": tourist.full_name if tourist else None,
            "emergency_contact_name": tourist.emergency_contact_name if tourist else None,
            "emergency_contact_phone": tourist.emergency_contact_phone if tourist else None
        } if tourist else None
    }
