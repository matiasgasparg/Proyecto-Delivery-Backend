from flask import request, jsonify
from ..models.pedido_model import Pedido
from ..models.exceptions import CustomException, InvalidDataError, ProductNotFound, DuplicateError
from ..models.pedidodetalle_model import PedidoDetalle

class PedidoController:
    @classmethod
    def get(cls, id_pedido):
        try:
            # Obtener el pedido por su ID
            pedido = Pedido.get(id_pedido)
            if not pedido:
                return jsonify({'error': 'Pedido no encontrado'}), 404
    
            # Obtener los detalles del pedido
            detalles = PedidoDetalle.get_by_pedido_id(id_pedido)
            serialized_detalles = [
                {
                    "id_plato": detalle.id_plato,
                    "cantidad": detalle.cantidad,
                    "comentario": detalle.comentario
                }
                for detalle in detalles
            ]
    
            # Serializar el pedido junto con sus detalles
            serialized_pedido = {
                "id_pedido": pedido.id_pedido,
                "id_cliente": pedido.id_cliente,
                "id_repartidor": pedido.id_repartidor,
                "domicilio_entrega": pedido.domicilio_entrega,
                "estado": pedido.estado,
                "fecha_hora": pedido.fecha_hora,
                "comentario": pedido.comentario,
                "detalles": serialized_detalles  # Incluir los detalles en la respuesta
            }
    
            return jsonify(serialized_pedido), 200
    
        except Exception as e:
            print(f"Error al obtener el pedido {id_pedido}: {str(e)}")
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
                    "pagado": pedido.pagado,  # Nuevo campo serializado
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
            print(f"Data recibida: {data}")  # Imprimir los datos recibidos
            
            if not data.get('id_cliente') or not data.get('domicilio_entrega') or not data.get('platos'):
                raise InvalidDataError("El id_cliente, domicilio_entrega y platos son obligatorios.")
        
            # Procesar el pedido
            new_pedido = Pedido(**data)  # Crear el pedido
            print(f"Nuevo pedido creado: {new_pedido}")  # Imprimir el nuevo pedido
            
            if Pedido.create(new_pedido):  # Crear el pedido en la base de datos
                return jsonify({'message': 'Pedido creado exitosamente'}), 201
            else:
                raise CustomException("Error al crear el pedido.")
        except InvalidDataError as e:
            return e.get_response()
        except CustomException as e:
            return jsonify({'error': str(e)}), 500
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
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
            valid_fields = ['estado', 'comentario', 'id_repartidor', 'pagado']

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
    @classmethod
    def modify_platos(cls, id_pedido):
        try:
            # Verificar si el pedido existe
            pedido = Pedido.get(id_pedido)
            if not pedido:
                raise ProductNotFound(id_pedido)
    
            # Obtener los datos de la solicitud
            data = request.json
            action = data.get('action')  # 'add' o 'remove'
            platos = data.get('platos')  # Lista de platos a agregar/eliminar
    
            if action not in ['add', 'remove']:
                raise InvalidDataError("La acción debe ser 'add' o 'remove'.")
    
            if not platos or not isinstance(platos, list):
                raise InvalidDataError("Debe proporcionar una lista de platos.")
    
            if action == 'add':
                # Agregar nuevos platos al pedido
                for plato in platos:
                    new_detalle = PedidoDetalle(
                        id_pedido=id_pedido,
                        id_plato=plato.get('id_plato'),
                        cantidad=plato.get('cantidad'),
                        comentario=plato.get('comentario', '')
                    )
                    PedidoDetalle.create(new_detalle)
    
            elif action == 'remove':
                # Eliminar platos del pedido
                for plato in platos:
                    PedidoDetalle.delete_by_pedido_id_and_plato(
                        id_pedido=id_pedido,
                        id_plato=plato.get('id_plato')
                    )
    
            return jsonify({'message': 'Pedido modificado exitosamente'}), 200
    
        except ProductNotFound as e:
            return e.get_response()
        except InvalidDataError as e:
            return e.get_response()
        except Exception as e:
            print(f"Error al modificar los platos del pedido {id_pedido}: {str(e)}")
            return jsonify({'error': 'Error en la solicitud'}), 500
    