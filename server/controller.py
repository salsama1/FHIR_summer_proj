from flask import request, jsonify
from fhir_creation import create_fhir_bundle
from fhir_validator_db import validate_fhir_resources_db
from pydantic import ValidationError
import logging
import traceback
from sql_con.connection import get_db
from sqlalchemy.orm import Session
from business_validation import validate_fhir_resources_business


logging.basicConfig(level=logging.DEBUG)

def handle_hello():
    return 'Hello Dear'

def handle_eligibility():
    data = request.get_json()
    logging.debug(f"Received data: {data}")

    try:
        bundle = create_fhir_bundle(data)
        
        patient = bundle.entry[0].resource
        insurer = bundle.entry[1].resource
        provider = bundle.entry[2].resource
        coverage = bundle.entry[3].resource
        eligibility_request = bundle.entry[4].resource


        business_errors = validate_fhir_resources_business(eligibility_request)
        if business_errors:
            return jsonify({"status": "Error", "message": "; ".join(business_errors)}), 400
        
        db = next(get_db())
        eligibility_response, error_message = validate_fhir_resources_db(db, patient, insurer, provider, coverage, eligibility_request)
        
        logging.debug(f"Eligibility response: {eligibility_response}, Error message: {error_message}")
        return jsonify(eligibility_response.dict()), 400 if error_message else 200

    except ValidationError as e:
        return jsonify({"status": "Validation error", "message": e.errors()}), 400
    except ValueError as ve:
        return jsonify({"status": "Validation error", "message": str(ve)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        logging.error(traceback.format_exc())
        return jsonify({"status": "Error", "message": str(e)}), 500
    finally:
        db.close()
