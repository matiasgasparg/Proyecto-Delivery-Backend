from flask import request, jsonify
from ..models.pedidopromocion_model import PedidoPromocion
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class PedidoPromocionController:
    @classmethod
    def get(cls, id_pedido_promocion):
        try:
            pedido_promocion = PedidoPromocion.get(id_pedido_promocion)
            if pedido_promocion:
                serialized_pedido_promocion = {
                    "id_pedido_promocion": pedido_promocion.id_pedido_promocion,
                    "id_pedido": pedido_promocion.id_pedido,
                    "id_promocion": pedido_promocion.id_promocion
                }
                return jsonify(serialized_pedido_promocion), 200
            else:
                raise ProductNotFound(id_pedido_promocion)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_pedido') or not data.get('id_promocion'):
                raise InvalidDataError("El id_pedido y id_promocion son obligatorios.")

            new_pedido_promocion = PedidoPromocion(**data)
            if PedidoPromocion.create(new_pedido_promocion):
                return jsonify({'message': 'Promoción asociada al pedido creada exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe una promoción asociada al mismo pedido.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_pedido_promocion):
        try:
            response, status_code = PedidoPromocion.delete(id_pedido_promocion)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
