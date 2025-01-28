from ..database import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash

class Cliente:
    def __init__(self, **kwargs):
        self.id_cliente = kwargs.get('id_cliente')
        self.nombre = kwargs.get('nombre')
        self.correo = kwargs.get('correo')
        self.domicilio = kwargs.get('domicilio')
        self.telefono = kwargs.get('telefono')
        self.contraseña = kwargs.get('contraseña')

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
            hashed_password = generate_password_hash(cliente.contraseña)

            query = """
                INSERT INTO Cliente (nombre, correo, domicilio, telefono,contraseña)
                VALUES (%s, %s, %s, %s,%s)
            """
            params = (cliente.nombre, cliente.correo, cliente.domicilio, cliente.telefono,hashed_password)
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
    def update(cls, id_plato, campo, nuevo_valor):
        try:
            # Validar el campo
            campos_validos = ['nombre', 'descripcion', 'precio', 'tipo_plato', 'disponible']
            if campo not in campos_validos:
                raise ValueError("Campo no válido para actualización")

            # Construir la consulta SQL de actualización
            query = f"UPDATE plato SET {campo} = %s WHERE id_plato = %s"
            params = (nuevo_valor, id_plato)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def get_by_email(cls, email):
        try:
            query = """
                SELECT id_cliente, nombre, correo, domicilio, telefono, contraseña
                FROM Cliente
                WHERE correo = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(email,))
            if result:
                return cls(
                    id_cliente=result[0], 
                    nombre=result[1], 
                    correo=result[2], 
                    domicilio=result[3], 
                    telefono=result[4], 
                    contraseña=result[5]  # Incluye la contraseña
                )
            return None
        except Exception as e:
            print(f"Error al obtener el cliente por email '{email}':", e)
            return None
        finally:
            DatabaseConnection.close_connection()
    