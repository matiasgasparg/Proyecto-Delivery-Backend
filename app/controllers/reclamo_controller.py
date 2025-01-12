from flask import request, jsonify
from ..models.reclamo_model import Reclamo
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound

class ReclamoController:
    @classmethod
    def get(cls, id_reclamo):
        try:
            reclamo = Reclamo.get(id_reclamo)
            if reclamo:
                serialized_reclamo = {
                    "id_reclamo": reclamo.id_reclamo,
                    "id_pedido": reclamo.id_pedido,
                    "descripcion": reclamo.descripcion,
                    "fecha_hora": reclamo.fecha_hora
                }
                return jsonify(serialized_reclamo), 200
            else:
                raise ProductNotFound(id_reclamo)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_pedido') or not data.get('descripcion'):
                raise InvalidDataError("El id_pedido y descripcion son obligatorios.")

            new_reclamo = Reclamo(**data)
            if Reclamo.create(new_reclamo):
                return jsonify({'message': 'Reclamo creado exitosamente'}), 201
            else:
                raise CustomException("No se pudo crear el reclamo.")
        except InvalidDataError as e:
            return e.get_response()
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_reclamo):
        try:
            response, status_code = Reclamo.delete(id_reclamo)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
