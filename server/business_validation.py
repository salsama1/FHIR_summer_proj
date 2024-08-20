from fhir.resources.coverageeligibilityrequest import CoverageEligibilityRequest
import logging

def validate_fhir_resources_business(eligibility_request: CoverageEligibilityRequest):
    errors = []

    if eligibility_request.extension:
        hospital_department_extension = next(
            (ext for ext in eligibility_request.extension if ext.url == "http://example.org/fhir/StructureDefinition/CoverageEligibilityRequestHospitalDepartmentExtension"),
            None
        )
        if not hospital_department_extension:
            errors.append("Hospital department extension is missing")
        else:
            value_string = getattr(hospital_department_extension, 'valueString', None)
            logging.debug(f"Hospital department valueString: {value_string} (Type: {type(value_string)})")
            if value_string is None:
                errors.append("Hospital department valueString is missing")
            elif not isinstance(value_string, str):
                errors.append(f"Hospital department is not a valid string, found type: {type(value_string).__name__}")
    else:
        errors.append("Hospital department extension is missing")

    logging.debug(f"Business validation errors: {errors}")
    return errors
