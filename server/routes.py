from flask import Blueprint
from controller import handle_eligibility

main = Blueprint('main', __name__)


@main.route('/eligibility', methods=['POST'])
def eligibility():
    return handle_eligibility()
