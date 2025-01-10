from ..database import DatabaseConnection
from flask import Flask, request, jsonify

class Plato:
    """
    Modelo que representa los platos en la base de datos y proporciona métodos
    para realizar operaciones CRUD sobre ellos.

    Atributos:
        - `id_plato` (int): ID del plato.
        - `nombre` (str): Nombre del plato.
        - `descripcion` (str): Descripción del plato.
        - `precio` (float): Precio del plato.
        - `disponible` (bool): Indica si el plato está disponible.
    """

    def __init__(self, **kwargs):
        """
        Constructor de la clase Plato.

        Args:
            **kwargs: Argumentos opcionales para inicializar el objeto Plato.
        """
        self.id_plato = kwargs.get('id_plato')
        self.nombre = kwargs.get('nombre')
        self.descripcion = kwargs.get('descripcion')
        self.precio = kwargs.get('precio')
        self.disponible = kwargs.get('disponible')

    @classmethod
    def get(cls, id_plato):
        """
        Obtiene un plato específico por su ID.

        Args:
            id_plato (int): ID del plato a obtener.

        Returns:
            Plato: Objeto Plato si se encuentra; de lo contrario, None.
        """
        try:
            query = """
                SELECT id_plato, nombre, descripcion, precio, disponible
                FROM plato
                WHERE id_plato = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_plato,))
            if result:
                id_plato, nombre, descripcion, precio, disponible = result
                return cls(id_plato=id_plato, nombre=nombre, descripcion=descripcion, precio=precio, disponible=disponible)
            return None
        except Exception as e:
            print("Error al obtener el plato:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        """
        Obtiene todos los platos disponibles en la base de datos.

        Returns:
            list: Lista de objetos Plato.
        """
        try:
            query = """
                SELECT id_plato, nombre, descripcion, precio, disponible
                FROM plato
            """
            results = DatabaseConnection.fetch_all(query)
            platos = [
                cls(id_plato=id_plato, nombre=nombre, descripcion=descripcion, precio=precio, disponible=disponible)
                for id_plato, nombre, descripcion, precio, disponible in results
            ]
            return platos
        except Exception as e:
            print("Error al obtener todos los platos:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, plato):
        """
        Crea un nuevo plato en la base de datos.

        Args:
            plato (Plato): Objeto Plato con los datos a insertar.

        Returns:
            bool: True si la operación fue exitosa; de lo contrario, False.
        """
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
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_plato):
        """
        Elimina un plato de la base de datos por su ID.

        Args:
            id_plato (int): ID del plato a eliminar.

        Returns:
            tuple: Mensaje de resultado y código de estado HTTP.
        """
        try:
            if not cls.exists(id_plato):
                raise ProductNotFound(id_plato)  # Lanza excepción si no existe.

            query = "DELETE FROM plato WHERE id_plato = %s"
            params = (id_plato,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Plato eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el plato:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_plato, campo, nuevo_valor):
        """
        Actualiza un campo específico de un plato.

        Args:
            id_plato (int): ID del plato a actualizar.
            campo (str): Nombre del campo a actualizar.
            nuevo_valor (any): Nuevo valor para el campo.

        Returns:
            str: Mensaje de resultado.
        """
        try:
            if not cls.exists(id_plato):
                raise ProductNotFound(id_plato)

            campos_validos = {
                'nombre': "UPDATE plato SET nombre = %s WHERE id_plato = %s",
                'descripcion': "UPDATE plato SET descripcion = %s WHERE id_plato = %s",
                'precio': "UPDATE plato SET precio = %s WHERE id_plato = %s",
                'disponible': "UPDATE plato SET disponible = %s WHERE id_plato = %s",
            }

            if campo not in campos_validos:
                raise ValueError("Campo no válido para actualización")

            query = campos_validos[campo]
            params = (nuevo_valor, id_plato)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def exists(cls, id_plato):
        """
        Verifica si un plato existe en la base de datos.

        Args:
            id_plato (int): ID del plato a verificar.

        Returns:
            bool: True si el plato existe; de lo contrario, False.
        """
        query = "SELECT COUNT(*) FROM plato WHERE id_plato = %s"
        params = (id_plato,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0
