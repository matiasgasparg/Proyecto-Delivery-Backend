from flask import request, jsonify
from ..models.cliente_model import Cliente
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class ClienteController:
    @classmethod
    def get(cls, id_cliente):
        try:
            cliente = Cliente.get(id_cliente)
            if cliente:
                serialized_cliente = {
                    "id_cliente": cliente.id_cliente,
                    "nombre": cliente.nombre,
                    "correo": cliente.correo,
                    "domicilio": cliente.domicilio,
                    "telefono": cliente.telefono
                }
                return jsonify(serialized_cliente), 200
            else:
                raise ProductNotFound(id_cliente)  # Excepción personalizada para el usuario no encontrado
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def get_by_email(cls,email):
        try:
            cliente = Cliente.get_by_email(email)  # Llama al método DAO
            if cliente:
                serialized_cliente = {
                    "id_cliente": cliente.id_cliente,
                    "nombre": cliente.nombre,
                    "correo": cliente.correo,
                    "domicilio": cliente.domicilio,
                    "telefono": cliente.telefono
                }
                return jsonify(serialized_cliente), 200
            else:
                raise ProductNotFound(email)  # Excepción personalizada para el cliente no encontrado
        except ProductNotFound as e:
            return e.get_response()  # Maneja la excepción personalizada
        except Exception as e:
            print(f"Error al procesar la solicitud para email '{email}':", e)
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def get_all(cls):
        try:
            clientes = Cliente.get_all()
            serialized_clientes = [
                {
                    "id_cliente": cliente.id_cliente,
                    "nombre": cliente.nombre,
                    "correo": cliente.correo,
                    "domicilio": cliente.domicilio,
                    "telefono": cliente.telefono
                } for cliente in clientes
            ]
            return jsonify(serialized_clientes), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('nombre') or not data.get('correo') or not data.get('telefono'):
                raise InvalidDataError("El nombre, correo y teléfono son obligatorios.")

            new_cliente = Cliente(**data)
            if Cliente.create(new_cliente):
                return jsonify({'message': 'Cliente creado exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe un cliente con el mismo correo.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_cliente):
        try:
            # Verificar si el cliente existe
            cliente = Cliente.get(id_cliente)
            if not cliente:
                raise ProductNotFound(id_cliente)  # Lanza un error si no existe el cliente

            # Si el cliente existe, proceder con la actualización
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['nombre', 'correo', 'domicilio', 'telefono']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Cliente.update(id_cliente, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_cliente):
        try:
            cliente=Cliente.get(id_cliente)
            if not cliente:
                raise ProductNotFound(f"Cliente con ID {id_cliente} no encontrado.")
            response, status_code = Cliente.delete(id_cliente)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para plato no encontrado.
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
