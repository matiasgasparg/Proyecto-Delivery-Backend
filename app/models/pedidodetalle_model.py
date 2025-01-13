from ..database import DatabaseConnection

class PedidoDetalle:
    def __init__(self, **kwargs):
        self.id_pedido_detalle = kwargs.get('id_pedido_detalle')
        self.id_pedido = kwargs.get('id_pedido')
        self.id_plato = kwargs.get('id_plato')
        self.cantidad = kwargs.get('cantidad')
        self.comentario = kwargs.get('comentario')

    @classmethod
    def get_by_pedido_id(cls, id_pedido):
        try:
            query = """
                SELECT id_pedido_detalle, id_plato, cantidad, comentario
                FROM PedidoDetalle
                WHERE id_pedido = %s
            """
            results = DatabaseConnection.fetch_all(query, params=(id_pedido,))
            return [
                cls(
                    id_pedido_detalle=row[0], id_plato=row[1],
                    cantidad=row[2], comentario=row[3]
                ) for row in results
            ]
        except Exception as e:
            print(f"Error al obtener detalles del pedido {id_pedido}: {e}")
            return []
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_pedido_detalle, id_pedido, id_plato, cantidad, comentario
                FROM PedidoDetalle
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_pedido_detalle=row[0], id_pedido=row[1], id_plato=row[2],
                    cantidad=row[3], comentario=row[4]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todos los detalles de los pedidos:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, pedido_detalle):
        try:
            query = """
                INSERT INTO PedidoDetalle (id_pedido, id_plato, cantidad, comentario)
                VALUES (%s, %s, %s, %s)
            """
            params = (
                pedido_detalle.id_pedido, pedido_detalle.id_plato,
                pedido_detalle.cantidad, pedido_detalle.comentario
            )
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el detalle del pedido:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_pedido_detalle):
        try:
            query = "DELETE FROM PedidoDetalle WHERE id_pedido_detalle = %s"
            params = (id_pedido_detalle,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Detalle del pedido eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el detalle del pedido:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_pedido_detalle, campo, nuevo_valor):
        try:
            query = f"UPDATE PedidoDetalle SET {campo} = %s WHERE id_pedido_detalle = %s"
            params = (nuevo_valor, id_pedido_detalle)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def delete_by_pedido_id_and_plato(cls, id_pedido, id_plato):
        try:
            query = "DELETE FROM PedidoDetalle WHERE id_pedido = %s AND id_plato = %s"
            params = (id_pedido, id_plato)
            DatabaseConnection.execute_query(query, params=params)
        except Exception as e:
            print(f"Error al eliminar el detalle del pedido {id_pedido} para el plato {id_plato}: {e}")
            raise Exception("No se pudo eliminar el detalle del pedido.")
        finally:
            DatabaseConnection.close_connection()
