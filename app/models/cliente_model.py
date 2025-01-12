from ..database import DatabaseConnection

class Cliente:
    def __init__(self, **kwargs):
        self.id_cliente = kwargs.get('id_cliente')
        self.nombre = kwargs.get('nombre')
        self.correo = kwargs.get('correo')
        self.domicilio = kwargs.get('domicilio')
        self.telefono = kwargs.get('telefono')

    @classmethod
    def get(cls, id_cliente):
        try:
            query = """
                SELECT id_cliente, nombre, correo, domicilio, telefono
                FROM Cliente
                WHERE id_cliente = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_cliente,))
            if result:
                return cls(id_cliente=result[0], nombre=result[1], correo=result[2], domicilio=result[3], telefono=result[4])
            return None
        except Exception as e:
            print("Error al obtener el cliente:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_cliente, nombre, correo, domicilio, telefono
                FROM Cliente
            """
            results = DatabaseConnection.fetch_all(query)
            return [cls(id_cliente=row[0], nombre=row[1], correo=row[2], domicilio=row[3], telefono=row[4]) for row in results]
        except Exception as e:
            print("Error al obtener todos los clientes:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, cliente):
        try:
            query = """
                INSERT INTO Cliente (nombre, correo, domicilio, telefono)
                VALUES (%s, %s, %s, %s)
            """
            params = (cliente.nombre, cliente.correo, cliente.domicilio, cliente.telefono)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el cliente:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_cliente):
        try:
            query = "DELETE FROM Cliente WHERE id_cliente = %s"
            params = (id_cliente,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Cliente eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el cliente:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_cliente, campo, nuevo_valor):
        try:
            query = f"UPDATE Cliente SET {campo} = %s WHERE id_cliente = %s"
            params = (nuevo_valor, id_cliente)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
