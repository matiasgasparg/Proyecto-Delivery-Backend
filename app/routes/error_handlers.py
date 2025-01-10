from flask import jsonify, Blueprint
from ..models.exceptions import CustomException, UserNotFound, InvalidDataError, DuplicateError

# Crear un Blueprint para manejar errores
errors = Blueprint("errors", __name__)

@errors.app_errorhandler(CustomException)
def handle_custom_exception(error):
    """
    Maneja errores personalizados definidos por la clase CustomException.

    Args:
        error (CustomException): La excepción personalizada generada.

    Returns:
        Response: Respuesta HTTP con el mensaje y código de estado definido en la excepción.
    """
    return error.get_response()

@errors.app_errorhandler(UserNotFound)
def handle_user_not_found(error):
    """
    Maneja errores relacionados con usuarios no encontrados.

    Args:
        error (UserNotFound): La excepción generada cuando no se encuentra un usuario.

    Returns:
        Response: Respuesta HTTP con el mensaje y código de estado definido en la excepción.
    """
    return error.get_response()

@errors.app_errorhandler(InvalidDataError)
def handle_invalid_data(error):
    """
    Maneja errores de datos inválidos en solicitudes.

    Args:
        error (InvalidDataError): La excepción generada por datos inválidos en una solicitud.

    Returns:
        Response: Respuesta HTTP con el mensaje y código de estado definido en la excepción.
    """
    return error.get_response()

@errors.app_errorhandler(DuplicateError)
def handle_duplicate_data(error):
    """
    Maneja errores de duplicados en los datos.

    Args:
        error (DuplicateError): La excepción generada cuando hay datos duplicados.

    Returns:
        Response: Respuesta HTTP con el mensaje y código de estado definido en la excepción.
    """
    return error.get_response()
