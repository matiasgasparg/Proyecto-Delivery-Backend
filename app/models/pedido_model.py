from ..database import DatabaseConnection

class Pedido:
    def __init__(self, **kwargs):
        self.id_pedido = kwargs.get('id_pedido')
        self.id_cliente = kwargs.get('id_cliente')
        self.id_repartidor = kwargs.get('id_repartidor')
        self.domicilio_entrega = kwargs.get('domicilio_entrega')
        self.estado = kwargs.get('estado', 'Pendiente')
        self.fecha_hora = kwargs.get('fecha_hora')
        self.comentario = kwargs.get('comentario')
        self.platos = kwargs.get('platos', [])  # Nueva propiedad para los platos del pedido

    @classmethod
    def get(cls, id_pedido):
        try:
            query = """
                SELECT id_pedido, id_cliente, id_repartidor, domicilio_entrega, estado, fecha_hora, comentario
                FROM Pedido
                WHERE id_pedido = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_pedido,))
            if result:
                return cls(
                    id_pedido=result[0], id_cliente=result[1], id_repartidor=result[2],
                    domicilio_entrega=result[3], estado=result[4],
                    fecha_hora=result[5], comentario=result[6]
                )
            return None
        except Exception as e:
            print("Error al obtener el pedido:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_pedido, id_cliente, id_repartidor, domicilio_entrega, estado, fecha_hora, comentario
                FROM Pedido
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_pedido=row[0], id_cliente=row[1], id_repartidor=row[2],
                    domicilio_entrega=row[3], estado=row[4],
                    fecha_hora=row[5], comentario=row[6]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todos los pedidos:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, pedido):
        try:
            # Primero, crear el pedido en la tabla Pedido
            query = """
                INSERT INTO Pedido (id_cliente, id_repartidor, domicilio_entrega, estado, comentario)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                pedido.id_cliente, pedido.id_repartidor, pedido.domicilio_entrega,
                pedido.estado, pedido.comentario
            )
            DatabaseConnection.execute_query(query, params=params)

            # Obtener el id del pedido recién creado
            query = "SELECT LAST_INSERT_ID()"
            result = DatabaseConnection.fetch_one(query)
            id_pedido = result[0]

            # Ahora crear los detalles del pedido
            for plato in pedido.platos:
                detalle_query = """
                    INSERT INTO PedidoDetalle (id_pedido, id_plato, cantidad, comentario)
                    VALUES (%s, %s, %s, %s)
                """
                detalle_params = (
                    id_pedido, plato['id_plato'], plato['cantidad'], plato.get('comentario', '')
                )
                DatabaseConnection.execute_query(detalle_query, params=detalle_params)

            return True
        except Exception as e:
            print("Error al crear el pedido:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_pedido):
        try:
            query = "DELETE FROM Pedido WHERE id_pedido = %s"
            params = (id_pedido,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Pedido eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el pedido:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_pedido, campo, nuevo_valor):
        try:
            query = f"UPDATE Pedido SET {campo} = %s WHERE id_pedido = %s"
            params = (nuevo_valor, id_pedido)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
