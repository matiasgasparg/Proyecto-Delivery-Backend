from ..database import DatabaseConnection
from ..models.exceptions import ProductNotFound, DuplicateError

class ComboPlato:
    def __init__(self, **kwargs):
        self.id_combo_plato = kwargs.get('id_combo_plato')
        self.id_promocion = kwargs.get('id_promocion')
        self.id_plato = kwargs.get('id_plato')

    @classmethod
    def get(cls, id_combo_plato):
        try:
            query = """
                SELECT id_combo_plato, id_promocion, id_plato
                FROM combo_plato
                WHERE id_combo_plato = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_combo_plato,))

            if result:
                id_combo_plato, id_promocion, id_plato = result
                combo_plato = cls(id_combo_plato=id_combo_plato, id_promocion=id_promocion, id_plato=id_plato)
                return combo_plato
            else:
                return None
        except Exception as e:
            print("Error al obtener el ComboPlato:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, combo_plato):
        try:
            query = """
                INSERT INTO combo_plato (id_promocion, id_plato)
                VALUES (%s, %s)
            """
            params = (combo_plato.id_promocion, combo_plato.id_plato)
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear el ComboPlato:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_combo_plato):
        try:
            # Verificar si el combo plato existe antes de eliminarlo
            if not cls.exists(id_combo_plato):
                raise ProductNotFound(id_combo_plato)

            query = "DELETE FROM combo_plato WHERE id_combo_plato = %s"
            params = (id_combo_plato,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'ComboPlato eliminado exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar el ComboPlato:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def exists(cls, id_combo_plato):
        query = "SELECT COUNT(*) FROM combo_plato WHERE id_combo_plato = %s"
        params = (id_combo_plato,)
        result = DatabaseConnection.fetch_one(query, params=params)
        return result[0] > 0
