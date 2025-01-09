from ..database import DatabaseConnection
from flask import Flask, request, jsonify

class Plato:
    def __init__(self, **kwargs):
        self.id_plato = kwargs.get('id_plato')
        self.nombre = kwargs.get('nombre')
        self.descripcion = kwargs.get('descripcion')
        self.precio = kwargs.get('precio')
        self.disponible = kwargs.get('disponible')

    @classmethod
    def get(cls, id_plato):
        try:
            query = """
                SELECT id_plato, nombre, descripcion, precio, disponible
                FROM plato
                WHERE id_plato = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_plato,))

            if result:
                id_plato, nombre, descripcion, precio, disponible = result
                plato = cls(id_plato=id_plato, nombre=nombre, descripcion=descripcion, precio=precio, disponible=disponible)
                return plato
            else:
                return None
        except Exception as e:
            print("Error al obtener el plato:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_plato, nombre, descripcion, precio, disponible
                FROM plato
            """
            results = DatabaseConnection.fetch_all(query)

            platos = []
            for result in results:
                id_plato, nombre, descripcion, precio, disponible = result
                plato = cls(id_plato=id_plato, nombre=nombre, descripcion=descripcion, precio=precio, disponible=disponible)
                platos.append(plato)

            return platos
        except Exception as e:
            print("Error al obtener todos los platos:", e)
            return None
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def create(cls, plato):
        try:
            query = """
                INSERT INTO plato (nombre, descripcion, precio, disponible)
                VALUES (%s, %s, %s, %s)
            """
            params = (plato.nombre, plato.descripcion, plato.precio, plato.disponible)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el plato:", e)
            return False
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def delete(cls, id_plato):
        try:
            # Verificar si el plato existe antes de eliminarlo
            if not cls.exists(id_plato):
                raise ProductNotFound(id_plato)  # Lanza la excepción si no existe

            query = "DELETE FROM plato WHERE id_plato = %s"
            params = (id_plato,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Plato eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el plato:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def update(cls, id_plato, campo, nuevo_valor):
        try:
            # Verificar si el plato existe antes de actualizarlo
            if not cls.exists(id_plato):
                raise ProductNotFound(id_plato)  # Lanza la excepción si no existe

            if campo == 'nombre':
                query = "UPDATE plato SET nombre = %s WHERE id_plato = %s"
            elif campo == 'descripcion':
                query = "UPDATE plato SET descripcion = %s WHERE id_plato = %s"
            elif campo == 'precio':
                query = "UPDATE plato SET precio = %s WHERE id_plato = %s"
            elif campo == 'disponible':
                query = "UPDATE plato SET disponible = %s WHERE id_plato = %s"
            else:
                raise ValueError("Campo no válido para actualización")

            params = (nuevo_valor, id_plato)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()  # Cerrar la conexión después de realizar la consulta

    @classmethod
    def exists(cls, id_plato):
        query = "SELECT COUNT(*) FROM plato WHERE id_plato = %s"
        params = (id_plato,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0
