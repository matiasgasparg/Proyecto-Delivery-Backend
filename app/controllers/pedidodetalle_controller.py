from flask import request, jsonify
from ..models.pedidodetalle_model import PedidoDetalle
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError

class PedidoDetalleController:
    @classmethod
    def get(cls, id_pedido_detalle):
        try:
            pedido_detalle = PedidoDetalle.get(id_pedido_detalle)
            if pedido_detalle:
                serialized_pedido_detalle = {
                    "id_pedido_detalle": pedido_detalle.id_pedido_detalle,
                    "id_pedido": pedido_detalle.id_pedido,
                    "id_plato": pedido_detalle.id_plato,
                    "cantidad": pedido_detalle.cantidad,
                    "comentario": pedido_detalle.comentario
                }
                return jsonify(serialized_pedido_detalle), 200
            else:
                raise ProductNotFound(id_pedido_detalle)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_pedido') or not data.get('id_plato'):
                raise InvalidDataError("El id_pedido y id_plato son obligatorios.")

            new_pedido_detalle = PedidoDetalle(**data)
            if PedidoDetalle.create(new_pedido_detalle):
                return jsonify({'message': 'Detalle de pedido creado exitosamente'}), 201
            else:
                raise DuplicateError("Ya existe un detalle con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_pedido_detalle):
        try:
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['cantidad', 'comentario']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = PedidoDetalle.update(id_pedido_detalle, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_pedido_detalle):
        try:
            response, status_code = PedidoDetalle.delete(id_pedido_detalle)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
