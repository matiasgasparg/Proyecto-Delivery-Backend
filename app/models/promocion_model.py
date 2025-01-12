from ..database import DatabaseConnection

class Promocion:
    def __init__(self, **kwargs):
        self.id_promocion = kwargs.get('id_promocion')
        self.tipo = kwargs.get('tipo')
        self.descripcion = kwargs.get('descripcion')
        self.monto_minimo = kwargs.get('monto_minimo')
        self.descuento_porcentaje = kwargs.get('descuento_porcentaje')
        self.disponible = kwargs.get('disponible', True)

    @classmethod
    def get(cls, id_promocion):
        try:
            query = """
                SELECT id_promocion, tipo, descripcion, monto_minimo, descuento_porcentaje, disponible
                FROM Promocion
                WHERE id_promocion = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_promocion,))
            if result:
                return cls(
                    id_promocion=result[0], tipo=result[1], descripcion=result[2],
                    monto_minimo=result[3], descuento_porcentaje=result[4], disponible=result[5]
                )
            return None
        except Exception as e:
            print("Error al obtener la promoción:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_promocion, tipo, descripcion, monto_minimo, descuento_porcentaje, disponible
                FROM Promocion
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_promocion=row[0], tipo=row[1], descripcion=row[2],
                    monto_minimo=row[3], descuento_porcentaje=row[4], disponible=row[5]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todas las promociones:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, promocion):
        try:
            query = """
                INSERT INTO Promocion (tipo, descripcion, monto_minimo, descuento_porcentaje, disponible)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                promocion.tipo, promocion.descripcion, promocion.monto_minimo,
                promocion.descuento_porcentaje, promocion.disponible
            )
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear la promoción:", e)
            return False
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def delete(cls, id_promocion):
        try:
            query = "DELETE FROM Promocion WHERE id_promocion = %s"
            params = (id_promocion,)
            DatabaseConnection.execute_query(query, params=params)
            return {'message': 'Promoción eliminada exitosamente'}, 204
        except Exception as e:
            print("Error al eliminar la promoción:", e)
            return {'message': 'Error en la solicitud'}, 500
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def update(cls, id_promocion, campo, nuevo_valor):
        try:
            query = f"UPDATE Promocion SET {campo} = %s WHERE id_promocion = %s"
            params = (nuevo_valor, id_promocion)
            DatabaseConnection.execute_query(query, params=params)
            return f'{campo.capitalize()} actualizado exitosamente'
        except Exception as e:
            print(f"Error al actualizar el campo '{campo}':", e)
            return 'Error en la solicitud'
        finally:
            DatabaseConnection.close_connection()
