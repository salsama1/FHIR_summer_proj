from fhir.resources.bundle import Bundle
from fhir.resources.patient import Patient
from fhir.resources.organization import Organization
from fhir.resources.coverageeligibilityrequest import CoverageEligibilityRequest
from fhir.resources.coverage import Coverage
from datetime import datetime
from fhir.resources.extension import Extension

def create_fhir_bundle(data):
    try:
        patient_data = {
            "resourceType": "Patient",
            "id": data['patient_id'],
            "name": [{
                "use": "official",
                "given": ["Placeholder"]  
            }],
            "birthDate": "1900-01-01"  
        }
        patient = Patient(**patient_data)

        insurer_data = {
            "resourceType": "Organization",
            "id": data['insurer_id'],
            "name": "Placeholder",  
            "type": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                    "code": "ins",
                    "display": "Insurance Company"
                }]
            }]
        }
        insurer = Organization(**insurer_data)

        provider_data = {
            "resourceType": "Organization",
            "id": 2,  
            "name": "Al-Habeeb Hospital",
            "type": [{
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/organization-type",
                    "code": "prov",
                    "display": "Healthcare Provider"
                }]
            }]
        }
        provider = Organization(**provider_data)

        coverage_data = {
            "resourceType": "Coverage",
            "id": 1,  
            "status": "active",
            "kind": "insurance",
            "beneficiary": {
                "reference": f"Patient/{data['patient_id']}"
            },
            "period": {
                "start": "2020-09-28",
                "end": "2022-09-30",
            },
            "insurer": {
                "reference": f"Organization/{data['insurer_id']}"
            }
        }
        coverage = Coverage(**coverage_data)

        eligibility_request_data = {
            "resourceType": "CoverageEligibilityRequest",
            "id": 1,
            "status": "active",
            "purpose": ["validation"],
            "patient": {
                "reference": f"Patient/{data['patient_id']}"
            },
            "created": datetime.now().strftime('%Y-%m-%d'),
            "insurer": {
                "reference": f"Organization/{data['insurer_id']}"
            },
            "provider": {
                "reference": f"Organization/1"
            },
            "extension": [
                Extension(
                    url="http://example.org/fhir/StructureDefinition/CoverageEligibilityRequestHospitalDepartmentExtension",
                    valueString="dental"
                )
            ]
        }
        eligibility_request = CoverageEligibilityRequest(**eligibility_request_data)

        bundle_data = {
            "resourceType": "Bundle",
            "type": "transaction",
            "entry": [
                {"resource": patient},
                {"resource": insurer},
                {"resource": provider},
                {"resource": coverage},
                {"resource": eligibility_request}
            ]
        }
        bundle = Bundle(**bundle_data)

        return bundle

    except Exception as e:
        raise Exception(str(e))
