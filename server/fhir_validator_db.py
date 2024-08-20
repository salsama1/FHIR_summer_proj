from sql_con.queries import get_patient, get_organization, get_provider_in_insurer_network, get_active_coverage
from eligibility_response import create_coverage_eligibility_response
from datetime import datetime
from sqlalchemy.orm import Session
from business_validation import validate_fhir_resources_business
from fhir.resources.coverageeligibilityrequest import CoverageEligibilityRequest
import logging

def create_error_response(patient, insurer, provider, coverage, message, status="entered-in-error"):
    return create_coverage_eligibility_response(
        patient, insurer, provider, coverage, "error", message, status
    )

def validate_fhir_resources_db(db: Session, patient, insurer, provider, coverage, eligibility_request: CoverageEligibilityRequest):
    errors = []

    business_errors = validate_fhir_resources_business(eligibility_request)
    errors.extend(business_errors)

    if errors:
        logging.debug(f"Business validation errors: {errors}")
        outcome = "error"
        message = "; ".join(errors)
        status = "entered-in-error"
        eligibility_response = create_coverage_eligibility_response(
            patient, insurer, provider, coverage, outcome, message
        )
        return eligibility_response, message

    db_patient = get_patient(db, patient.id)
    if not db_patient:
        errors.append("Patient not found")

    db_insurer = get_organization(db, insurer.id)
    if not db_insurer:
        errors.append("Insurer not found")

    db_provider = get_organization(db, provider.id)
    if not db_provider:
        errors.append("Provider not found")

    if db_insurer and db_provider:
        db_network = get_provider_in_insurer_network(db, db_insurer.id, db_provider.id)
        if not db_network:
            errors.append("Provider not in insurer's network")
    else:
        db_network = None

    current_date = datetime.today().date()
    end_date = coverage.period.end

    if db_patient and db_insurer:
        db_coverage = get_active_coverage(db, db_patient.id, db_insurer.id, coverage.status, end_date)
    else:
        db_coverage = None

    if not db_coverage:
        errors.append("Not eligible for coverage")



    if errors:
        outcome = "error"
        message = "; ".join(errors)
        status = "entered-in-error"  
    else:
        outcome = "complete"
        message = "Eligible for coverage"
        status = "active"

    eligibility_response = create_coverage_eligibility_response(
        patient, insurer, provider, coverage, outcome, message
    )

    return eligibility_response, None if outcome == "complete" else message
