from sqlalchemy.orm import Session
from model.models import Patient, Organization, ProviderNetwork, Coverage
from datetime import datetime

def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()

def get_organization(db: Session, org_id: int):
    return db.query(Organization).filter(Organization.id == org_id).first()

def get_provider_in_insurer_network(db: Session, insurer_id: int, provider_id: int):
    return db.query(ProviderNetwork).filter(
        ProviderNetwork.insurer_id == insurer_id,
        ProviderNetwork.provider_id == provider_id
    ).first()

def get_active_coverage(db: Session, patient_id: int, insurer_id: int, status: str, end_date: datetime):
    current_date = datetime.today().date()
    return db.query(Coverage).filter(
        Coverage.patient_id == patient_id,
        Coverage.insurer_id == insurer_id,
        Coverage.status == 'active',
        Coverage.start_date <= current_date,
        Coverage.end_date >= current_date
    ).first()
