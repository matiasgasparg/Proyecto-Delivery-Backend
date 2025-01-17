from ..database import DatabaseConnection

class Repartidor:
    def __init__(self, **kwargs):
        self.id_repartidor = kwargs.get('id_repartidor')
        self.nombre = kwargs.get('nombre')
        self.telefono = kwargs.get('telefono')
        self.disponible = kwargs.get('disponible', True)  # Aseguramos que disponible tenga un valor por defecto

    @classmethod
    def get(cls, id_repartidor):
        try:
            query = """
                SELECT id_repartidor, nombre, telefono, disponible
                FROM Repartidor
                WHERE id_repartidor = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_repartidor,))
            if result:
                return cls(id_repartidor=result[0], nombre=result[1], telefono=result[2], disponible=result[3])
            return None
        except Exception as e:
            print("Error al obtener el repartidor:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_repartidor, nombre, telefono, disponible
                FROM Repartidor
            """
            results = DatabaseConnection.fetch_all(query)
            return [cls(id_repartidor=row[0], nombre=row[1], telefono=row[2], disponible=row[3]) for row in results]
        except Exception as e:
            print("Error al obtener todos los repartidores:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, repartidor):
        try:
            query = """
                INSERT INTO Repartidor (nombre, telefono, disponible)
                VALUES (%s, %s, %s)
            """
            params = (repartidor.nombre, repartidor.telefono, repartidor.disponible)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el repartidor:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_repartidor):
        try:
            query = "DELETE FROM Repartidor WHERE id_repartidor = %s"
            params = (id_repartidor,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Repartidor eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el repartidor:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_repartidor, campo, nuevo_valor):
        try:
            query = f"UPDATE Repartidor SET {campo} = %s WHERE id_repartidor = %s"
            params = (nuevo_valor, id_repartidor)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def get_by_name(cls, nombre):
        try:
            query = """
                SELECT id_repartidor, nombre, telefono
                FROM Repartidor
                WHERE nombre = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(nombre,))
            if result:
                return cls(id_repartidor=result[0], nombre=result[1], telefono=result[2])
            return None
        except Exception as e:
            print("Error al obtener el repartidor por nombre:", e)
            return None
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def get_by_disponibilidad(cls, disponible):
        try:
            query = """
                SELECT id_repartidor, nombre, telefono, disponible
                FROM Repartidor
                WHERE disponible = %s
            """
            results = DatabaseConnection.fetch_all(query, params=(disponible,))
            return [cls(id_repartidor=row[0], nombre=row[1], telefono=row[2], disponible=row[3]) for row in results]
        except Exception as e:
            print("Error al obtener repartidores por disponibilidad:", e)
            return []
        finally:
            DatabaseConnection.close_connection()
