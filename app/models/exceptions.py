from flask import jsonify

class CustomException(Exception):
    """Clase base para excepciones personalizadas."""
    def __init__(self, status_code, name="Custom Error", description="Error"):
        super().__init__()
        self.status_code = status_code
        self.name = name
        self.description = description

    def get_response(self):
        """
        Genera una respuesta JSON basada en la excepción personalizada.
        """
        response = jsonify({
            'error': {
                'code': self.status_code,
                'name': self.name,
                'description': self.description,
            }
        })
        response.status_code = self.status_code
        return response


class ProductNotFound(CustomException):
    """Excepción para cuando no se encuentra un producto."""
    def __init__(self, product_id):
        super().__init__(404, "Product Not Found", f"Product with ID {product_id} not found")


class UserNotFound(CustomException):
    """Excepción para cuando no se encuentra un usuario."""
    def __init__(self, user_id):
        super().__init__(404, "User Not Found", f"User with ID {user_id} not found")


class InvalidDataError(CustomException):
    """Excepción para datos inválidos proporcionados por el cliente."""
    def __init__(self, description="Invalid input data provided"):
        super().__init__(400, "Invalid Data", description)


class DuplicateError(CustomException):
    """Excepción para casos de datos duplicados en la base de datos."""
    def __init__(self, description="Duplicate data found"):
        super().__init__(409, "Duplicate Error", description)
