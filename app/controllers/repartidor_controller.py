from flask import request, jsonify
from ..models.repartidor_model import Repartidor
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class RepartidorController:
    @classmethod
    def get(cls, id_repartidor):
        try:
            repartidor = Repartidor.get(id_repartidor)
            if repartidor:
                serialized_repartidor = {
                    "id_repartidor": repartidor.id_repartidor,
                    "nombre": repartidor.nombre,
                    "telefono": repartidor.telefono,
                    "disponible": repartidor.disponible  # Incluyendo el campo disponible
                }
                return jsonify(serialized_repartidor), 200
            else:
                raise ProductNotFound(id_repartidor)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            repartidores = Repartidor.get_all()
            serialized_repartidores = [
                {
                    "id_repartidor": repartidor.id_repartidor,
                    "nombre": repartidor.nombre,
                    "telefono": repartidor.telefono,
                    "disponible": repartidor.disponible  # Incluyendo el campo disponible
                } for repartidor in repartidores
            ]
            return jsonify(serialized_repartidores), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('nombre') or not data.get('telefono'):
                raise InvalidDataError("El nombre y teléfono son obligatorios.")
            
            # Verificar si ya existe un repartidor con el mismo nombre
            existing_repartidor = Repartidor.get_by_name(data.get('nombre'))
            if existing_repartidor:
                raise DuplicateError(f"Ya existe un repartidor con el nombre '{data.get('nombre')}'.")

            new_repartidor = Repartidor(**data)
            if Repartidor.create(new_repartidor):
                return jsonify({'message': 'Repartidor creado exitosamente'}), 201
            else:
                raise DuplicateError("Error al crear el repartidor.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500


    @classmethod
    def update(cls, id_repartidor):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['nombre', 'telefono', 'disponible']  # Agregando 'disponible' como campo actualizable

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Repartidor.update(id_repartidor, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_repartidor):
        try:
            repartidor = Repartidor.get(id_repartidor)
            if not repartidor:
                raise ProductNotFound(f"Repartidor con ID {id_repartidor} no encontrado.")
            
            response, status_code = Repartidor.delete(id_repartidor)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()  # Devolver 404 con el mensaje de error adecuado
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500