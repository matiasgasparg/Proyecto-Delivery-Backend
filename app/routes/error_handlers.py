from flask import jsonify, Blueprint
from ..models.exceptions import CustomException, UserNotFound, InvalidDataError, DuplicateError

errors = Blueprint("errors", __name__)

@errors.app_errorhandler(CustomException)
def handle_custom_exception(error):
    return error.get_response()

@errors.app_errorhandler(UserNotFound)
def handle_user_not_found(error):
    return error.get_response()

@errors.app_errorhandler(InvalidDataError)
def handle_invalid_data(error):
    return error.get_response()
@errors.app_errorhandler(DuplicateError)
def handle_duplicate_data(error):
    return error.get_response()