from flask import request, jsonify
from ..models.pedido_model import Pedido
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError
from ..models.pedidodetalle_model import PedidoDetalle

class PedidoController:
    @classmethod
    def get(cls, id_pedido):
        try:
            pedido = Pedido.get(id_pedido)
            if pedido:
                serialized_pedido = {
                    "id_pedido": pedido.id_pedido,
                    "id_cliente": pedido.id_cliente,
                    "id_repartidor": pedido.id_repartidor,
                    "domicilio_entrega": pedido.domicilio_entrega,
                    "estado": pedido.estado,
                    "fecha_hora": pedido.fecha_hora,
                    "comentario": pedido.comentario
                }
                return jsonify(serialized_pedido), 200
            else:
                raise ProductNotFound(id_pedido)
        except ProductNotFound as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def get_all(cls):
        try:
            pedidos = Pedido.get_all()  # Obtener todos los pedidos
            serialized_pedidos = []
            
            for pedido in pedidos:
                # Serializamos los detalles del pedido
                detalles = PedidoDetalle.get_by_pedido_id(pedido.id_pedido)  # Obtener detalles del pedido
                serialized_detalles = [
                    {
                        "id_plato": detalle.id_plato,
                        "cantidad": detalle.cantidad,
                        "comentario": detalle.comentario
                    }
                    for detalle in detalles
                ]
                
                # Serializar el pedido con sus detalles
                serialized_pedido = {
                    "id_pedido": pedido.id_pedido,
                    "id_cliente": pedido.id_cliente,
                    "id_repartidor": pedido.id_repartidor,
                    "domicilio_entrega": pedido.domicilio_entrega,
                    "estado": pedido.estado,
                    "fecha_hora": pedido.fecha_hora,
                    "comentario": pedido.comentario,
                    "detalles": serialized_detalles  # Incluir detalles del pedido
                }
                
                serialized_pedidos.append(serialized_pedido)

            return jsonify(serialized_pedidos), 200

        except Exception as e:
            print(f"Error al obtener los pedidos: {str(e)}")
            return jsonify({'error': 'Error en la solicitud'}), 500
    @classmethod
    def create(cls):
        try:
            data = request.json
            if not data.get('id_cliente') or not data.get('domicilio_entrega') or not data.get('platos'):
                raise InvalidDataError("El id_cliente, domicilio_entrega y platos son obligatorios.")

            # Crear el nuevo pedido
            new_pedido = Pedido(**data)
            if Pedido.create(new_pedido):
                # Ahora agregamos los detalles del pedido (los platos)
                for plato in data['platos']:
                    detalle_data = {
                        'id_pedido': new_pedido.id_pedido,  # Usamos el id del pedido recién creado
                        'id_plato': plato['id_plato'],
                        'cantidad': plato['cantidad'],
                        'comentario': plato.get('comentario', '')  # Usamos un comentario vacío si no se proporciona
                    }
 

                return jsonify({'message': 'Pedido creado exitosamente con detalles'}), 201
            else:
                raise DuplicateError("Ya existe un pedido con los mismos datos.")
        except InvalidDataError as e:
            return e.get_response()
        except DuplicateError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def update(cls, id_pedido):
        try:
            # Verificar si el pedido existe
            pedido = Pedido.get(id_pedido)
            if not pedido:
                raise ProductNotFound(id_pedido)  # Lanza un error si no existe el pedido

            # Si el pedido existe, proceder con la actualización
            data = request.json
            field_to_update = data.get('field')
            value = data.get('value')
            valid_fields = ['estado', 'comentario', 'id_repartidor']

            if field_to_update not in valid_fields:
                raise InvalidDataError(f"'{field_to_update}' no es un campo válido para actualizar.")

            response = Pedido.update(id_pedido, field_to_update, value)
            return jsonify({'message': response}), 200
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para pedido no encontrado.
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500

    @classmethod
    def delete(cls, id_pedido):
        try:
            response, status_code = Pedido.delete(id_pedido)
            return jsonify(response), status_code
        except ProductNotFound as e:
            return e.get_response()  # Respuesta personalizada para pedido no encontrado.
        except Exception as e:
            return jsonify({'error': 'Error en la solicitud'}), 500
