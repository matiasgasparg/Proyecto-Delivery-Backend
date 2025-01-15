from ..database import DatabaseConnection
from werkzeug.security import generate_password_hash, check_password_hash

class Admin:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.dni = kwargs.get('dni')
        self.contraseña = kwargs.get('contraseña')

    @classmethod
    def get_by_dni(cls, dni):
        try:
            query = """
                SELECT id, dni, contraseña
                FROM Admin
                WHERE dni = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(dni,))
            if result:
                return cls(id=result[0], dni=result[1], contraseña=result[2])
            return None
        except Exception as e:
            print(f"Error al obtener el admin por DNI '{dni}':", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, admin):
        try:
            hashed_password = generate_password_hash(admin.contraseña)
            query = """
                INSERT INTO Admin (dni, contraseña)
                VALUES (%s, %s)
            """
            params = (admin.dni, hashed_password)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el administrador:", e)
            return False
        finally:
            DatabaseConnection.close_connection()
