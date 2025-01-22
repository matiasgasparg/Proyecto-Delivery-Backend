from ..database import DatabaseConnection

class Pedido:
    def __init__(self, **kwargs):
        self.id_pedido = kwargs.get('id_pedido')
        self.id_cliente = kwargs.get('id_cliente')
        self.id_repartidor = kwargs.get('id_repartidor')
        self.domicilio_entrega = kwargs.get('domicilio_entrega')
        self.estado = kwargs.get('estado', 'Pendiente')
        self.fecha_hora = kwargs.get('fecha_hora')
        self.comentario = kwargs.get('comentario')
        self.platos = kwargs.get('platos', [])  # Nueva propiedad para los platos del pedido
        self.pagado = kwargs.get('pagado', 2)  # Nuevo atributo

    @classmethod
    def get(cls, id_pedido):
        try:
            query = """
                SELECT id_pedido, id_cliente, id_repartidor, domicilio_entrega, estado, fecha_hora, comentario, pagado
                FROM Pedido
                WHERE id_pedido = %s
            """
            result = DatabaseConnection.fetch_one(query, params=(id_pedido,))
            if result:
                return cls(
                    id_pedido=result[0], id_cliente=result[1], id_repartidor=result[2],
                    domicilio_entrega=result[3], estado=result[4],
                    fecha_hora=result[5], comentario=result[6], pagado=result[7]
                )
            return None
        except Exception as e:
            print("Error al obtener el pedido:", e)
            return None
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def get_all(cls):
        try:
            query = """
                SELECT id_pedido, id_cliente, id_repartidor, domicilio_entrega, estado, fecha_hora, comentario, pagado
                FROM Pedido
            """
            results = DatabaseConnection.fetch_all(query)
            return [
                cls(
                    id_pedido=row[0], id_cliente=row[1], id_repartidor=row[2],
                    domicilio_entrega=row[3], estado=row[4],
                    fecha_hora=row[5], comentario=row[6], pagado=row[7]
                ) for row in results
            ]
        except Exception as e:
            print("Error al obtener todos los pedidos:", e)
            return []
        finally:
            DatabaseConnection.close_connection()

    @classmethod
    def create(cls, pedido):
        try:
            # Crear el pedido en la tabla Pedido
            query = """
                INSERT INTO Pedido (id_cliente, id_repartidor, domicilio_entrega, estado, comentario, pagado)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                pedido.id_cliente, pedido.id_repartidor, pedido.domicilio_entrega,
                pedido.estado, pedido.comentario, pedido.pagado
            )
            DatabaseConnection.execute_query(query, params=params)
    
            # Obtener el ID del pedido recién creado
            query = "SELECT LAST_INSERT_ID()"
            result = DatabaseConnection.fetch_one(query)
            id_pedido = result[0]
            pedido.id_pedido = id_pedido  # Actualizamos el ID del pedido
    
            # Crear los detalles del pedido
            for plato in pedido.platos:
                detalle_query = """
                    INSERT INTO PedidoDetalle (id_pedido, id_plato, cantidad, comentario)
                    VALUES (%s, %s, %s, %s)
                """
                detalle_params = (
                    id_pedido, plato['id_plato'], plato['cantidad'], plato.get('comentario', '')
                )
                try:
                    DatabaseConnection.execute_query(detalle_query, params=detalle_params)
                except Exception as e:
                    print(f"Error al crear el detalle del pedido para el plato {plato['id_plato']}: {e}")
                    raise Exception(f"No se pudo crear el detalle para el plato {plato['id_plato']}.")
    
            return True  # Si todo se ejecutó correctamente
    
        except Exception as e:
            print("Error al crear el pedido:", e)
            return False
        finally:
            DatabaseConnection.close_connection()
    @classmethod
    def delete_by_pedido_id(cls, id_pedido):
        try:
            query = "DELETE FROM PedidoDetalle WHERE id_pedido = %s"
            params = (id_pedido,)
            DatabaseConnection.execute_query(query, params=params)
        except Exception as e:
            print(f"Error al eliminar detalles para el pedido {id_pedido}: {e}")
            raise Exception("No se pudieron eliminar los detalles del pedido.")
        finally:
            DatabaseConnection.close_connection()
    

    @classmethod
    def update(cls, id_pedido, field, value):
        
        try:
            # Construir la consulta de actualización dinámicamente
            query = f"UPDATE Pedido SET {field} = %s WHERE id_pedido = %s"
            params = (value, id_pedido)
            DatabaseConnection.execute_query(query, params=params)
            return f"Pedido {id_pedido} actualizado exitosamente."
        except Exception as e:
            print(f"Error al actualizar el pedido {id_pedido}: {e}")
            raise Exception("Error al actualizar el pedido.")
        finally:
            DatabaseConnection.close_connection()
