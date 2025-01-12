from ..database import DatabaseConnection

class Opinion:
    def __init__(self, **kwargs):
        self.id_opinion = kwargs.get('id_opinion')
        self.id_pedido = kwargs.get('id_pedido')
        self.puntuacion = kwargs.get('puntuacion')
        self.comentario = kwargs.get('comentario')
        self.fecha_hora = kwargs.get('fecha_hora')

    @classmethod
    def get(cls, id_opinion):
        try:
            query = """
                SELECT id_opinion, id_pedido, puntuacion, comentario, fecha_hora
                FROM Opinion
                WHERE id_opinion = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_opinion,))
            if result:
                return cls(
                    id_opinion=result[0], id_pedido=result[1],
                    puntuacion=result[2], comentario=result[3], fecha_hora=result[4]
                )
            return None
        except Exception as e:
            print("Error al obtener la opinión:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_opinion, id_pedido, puntuacion, comentario, fecha_hora
                FROM Opinion
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_opinion=row[0], id_pedido=row[1],
                    puntuacion=row[2], comentario=row[3], fecha_hora=row[4]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todas las opiniones:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, opinion):
        try:
            query = """
                INSERT INTO Opinion (id_pedido, puntuacion, comentario)
                VALUES (%s, %s, %s)
            """
            params = (opinion.id_pedido, opinion.puntuacion, opinion.comentario)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear la opinión:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_opinion):
        try:
            query = "DELETE FROM Opinion WHERE id_opinion = %s"
            params = (id_opinion,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Opinión eliminada exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar la opinión:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_opinion, campo, nuevo_valor):
        try:
            query = f"UPDATE Opinion SET {campo} = %s WHERE id_opinion = %s"
            params = (nuevo_valor, id_opinion)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
