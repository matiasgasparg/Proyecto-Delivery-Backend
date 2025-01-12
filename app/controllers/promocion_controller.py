from flask import request, jsonify
from ..models.promocion_model import Promocion
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class PromocionController:
    @classmethod
    def get(cls, id_promocion):
        try:
            promocion = Promocion.get(id_promocion)
            if promocion:
                serialized_promocion = {
                    "id_promocion": promocion.id_promocion,
                    "tipo": promocion.tipo,
                    "descripcion": promocion.descripcion,
                    "monto_minimo": promocion.monto_minimo,
                    "descuento_porcentaje": promocion.descuento_porcentaje,
                    "disponible": promocion.disponible
                }
                return jsonify(serialized_promocion), 200
            else:
                raise ProductNotFound(id_promocion)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            promociones = Promocion.get_all()
            serialized_promociones = [
                {
                    "id_promocion": promocion.id_promocion,
                    "tipo": promocion.tipo,
                    "descripcion": promocion.descripcion,
                    "monto_minimo": promocion.monto_minimo,
                    "descuento_porcentaje": promocion.descuento_porcentaje,
                    "disponible": promocion.disponible
                } for promocion in promociones
            ]
            return jsonify(serialized_promociones), 200
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('tipo') or not data.get('descripcion'):
                raise InvalidDataError("Tipo y descripción son obligatorios.")

            new_promocion = Promocion(**data)
            if Promocion.create(new_promocion):
                return jsonify({'message': 'Promoción creada exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe una promoción con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_promocion):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['tipo', 'descripcion', 'monto_minimo', 'descuento_porcentaje', 'disponible']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Promocion.update(id_promocion, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_promocion):
        try:
            response, status_code = Promocion.delete(id_promocion)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
