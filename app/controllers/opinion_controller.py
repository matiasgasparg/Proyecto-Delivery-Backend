from flask import request, jsonify
from ..models.opinion_model import Opinion
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound

class OpinionController:
    @classmethod
    def get(cls, id_opinion):
        try:
            opinion = Opinion.get(id_opinion)
            if opinion:
                serialized_opinion = {
                    "id_opinion": opinion.id_opinion,
                    "id_pedido": opinion.id_pedido,
                    "puntuacion": opinion.puntuacion,
                    "comentario": opinion.comentario,
                    "fecha_hora": opinion.fecha_hora
                }
                return jsonify(serialized_opinion), 200
            else:
                raise ProductNotFound(id_opinion)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_pedido') or not data.get('puntuacion'):
                raise InvalidDataError("El id_pedido y puntuacion son obligatorios.")

            new_opinion = Opinion(**data)
            if Opinion.create(new_opinion):
                return jsonify({'message': 'Opinión creada exitosamente'}), 201
            else:
                raise CustomException("No se pudo crear la opinión.")
        except InvalidDataError as e:
            return e.get_response()
        except CustomException as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_opinion):
        try:
            response, status_code = Opinion.delete(id_opinion)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
