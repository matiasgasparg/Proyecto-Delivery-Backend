from flask import request, jsonify
from ..models.admin_model import Admin
from ..models.exceptions import InvalidDataError
from werkzeug.security import check_password_hash

class AdminController:
    @classmethod
    def login(cls):
        try:
            data = request.json
            dni = data.get('dni')
            contraseña = data.get('contraseña')

            if not dni or not contraseña:
                raise InvalidDataError("DNI y contraseña son obligatorios.")

            admin = Admin.get_by_dni(dni)
            if admin and check_password_hash(admin.contraseña, contraseña):
                return jsonify({'message': 'Login exitoso'}), 200
            else:
                return jsonify({'error': 'DNI o contraseña incorrectos'}), 401
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            print("Error al procesar la solicitud:", e)
            return jsonify({'error': f'Error en la solicitud: {str(e)}'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            dni = data.get('dni')
            contraseña = data.get('contraseña')

            if not dni or not contraseña:
                raise InvalidDataError("DNI y contraseña son obligatorios.")

            new_admin = Admin(dni=dni, contraseña=contraseña)
            if Admin.create(new_admin):
                return jsonify({'message': 'Administrador creado exitosamente'}), 201
            else:
                return jsonify({'error': 'Error al crear el administrador'}), 500
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
