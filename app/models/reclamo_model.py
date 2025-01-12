from ..database import DatabaseConnection

class Reclamo:
    def __init__(self, **kwargs):
        self.id_reclamo = kwargs.get('id_reclamo')
        self.id_pedido = kwargs.get('id_pedido')
        self.descripcion = kwargs.get('descripcion')
        self.fecha_hora = kwargs.get('fecha_hora')

    @classmethod
    def get(cls, id_reclamo):
        try:
            query = """
                SELECT id_reclamo, id_pedido, descripcion, fecha_hora
                FROM Reclamo
                WHERE id_reclamo = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_reclamo,))
            if result:
                return cls(
                    id_reclamo=result[0], id_pedido=result[1],
                    descripcion=result[2], fecha_hora=result[3]
                )
            return None
        except Exception as e:
            print("Error al obtener el reclamo:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_reclamo, id_pedido, descripcion, fecha_hora
                FROM Reclamo
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_reclamo=row[0], id_pedido=row[1],
                    descripcion=row[2], fecha_hora=row[3]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todos los reclamos:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, reclamo):
        try:
            query = """
                INSERT INTO Reclamo (id_pedido, descripcion)
                VALUES (%s, %s)
            """
            params = (reclamo.id_pedido, reclamo.descripcion)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el reclamo:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_reclamo):
        try:
            query = "DELETE FROM Reclamo WHERE id_reclamo = %s"
            params = (id_reclamo,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Reclamo eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el reclamo:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_reclamo, campo, nuevo_valor):
        try:
            query = f"UPDATE Reclamo SET {campo} = %s WHERE id_reclamo = %s"
            params = (nuevo_valor, id_reclamo)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
