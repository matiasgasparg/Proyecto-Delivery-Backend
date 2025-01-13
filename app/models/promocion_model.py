from ..database import DatabaseConnection
from ..models.plato_model import Plato

class Promocion:
    def __init__(self, id_promocion=None, tipo=None, descripcion=None, monto_minimo=None, descuento_porcentaje=None, precio=None, disponible=True, id_plato=None):
        self.id_promocion = id_promocion
        self.tipo = tipo
        self.descripcion = descripcion
        self.monto_minimo = monto_minimo
        self.descuento_porcentaje = descuento_porcentaje
        self.precio = precio
        self.disponible = disponible
        self.id_plato = id_plato  # Este es el plato que se asociará con la promoción
        self.plato = None  # Inicializamos el plato como None

    @classmethod
    def create(cls, promocion):
        try:
            query = """
                INSERT INTO Promocion (tipo, descripcion, monto_minimo, descuento_porcentaje, precio, disponible, id_plato)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                promocion.tipo, promocion.descripcion, promocion.monto_minimo,
                promocion.descuento_porcentaje, promocion.precio, promocion.disponible, promocion.id_plato
            )
            DatabaseConnection.execute_query(query, params=params)
            return True
        except Exception as e:
            print("Error al crear la promoción:", e)
            return False

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT p.id_promocion, p.tipo, p.descripcion, p.monto_minimo, p.descuento_porcentaje, p.precio, p.disponible, p.id_plato
                FROM Promocion p
            """
            results = DatabaseConnection.fetch_all(query)

            promociones = []
            for row in results:
                promocion = cls(
                    id_promocion=row[0],
                    tipo=row[1],
                    descripcion=row[2],
                    monto_minimo=row[3],
                    descuento_porcentaje=row[4],
                    precio=row[5],
                    disponible=row[6],
                    id_plato=row[7]  # Aquí asignamos el id_plato desde la consulta
                )

                # Si hay un plato asociado, obtenemos los detalles del plato
                if promocion.id_plato:
                    plato = Plato.get(promocion.id_plato)  # Llamamos a Plato.get con el id_plato
                    if plato:
                        promocion.plato = plato  # Guardamos el plato completo en el objeto promocion

                promociones.append(promocion)

            return promociones
        except Exception as e:
            print("Error al obtener promociones:", e)
            return []
        finally:
            DatabaseConnection.close_connection()
