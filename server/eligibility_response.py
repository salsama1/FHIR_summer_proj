from datetime import datetime
from fhir.resources.coverageeligibilityresponse import CoverageEligibilityResponse
from fhir.resources.reference import Reference
import uuid

def create_coverage_eligibility_response(patient, insurer, provider, coverage, outcome, message):
    status = "active" if outcome == "complete" else "entered-in-error"
    
    return CoverageEligibilityResponse(
        id=str(uuid.uuid4()),
        status=status,
        purpose=["validation"],
        patient=Reference(reference=f"Patient/{patient.id}"),
        requestor=Reference(reference=f"Organization/{provider.id}"),
        request=Reference(reference=f"CoverageEligibilityRequest/{coverage.id}"),
        created=datetime.now().strftime('%Y-%m-%d'),
        insurer=Reference(reference=f"Organization/{insurer.id}"),
        outcome=outcome,
        disposition=message
    )
