import mysql.connector

class DatabaseConnection:
    """
    Clase para gestionar la conexión a una base de datos MySQL utilizando el patrón Singleton.
    Permite ejecutar consultas y manejar la conexión de manera centralizada.
    
    """

    # Atributo estático para almacenar la conexión única
    _connection = None

    # Atributo estático para almacenar la configuración de la base de datos
    _config = None

    @classmethod
    def get_connection(cls):
        """
        Obtiene la conexión única a la base de datos. Si no existe una conexión, la crea.

        Returns:
            mysql.connector.connection: La conexión activa a la base de datos.
        """
        if cls._connection is None:
            try:
                # Crear la conexión a la base de datos utilizando la configuración proporcionada
                cls._connection = mysql.connector.connect(
                    host=cls._config['DATABASE_HOST'],
                    user=cls._config['DATABASE_USERNAME'],
                    password=cls._config['DATABASE_PASSWORD'],
                    database=cls._config['DATABASE_NAME']
                )
            except mysql.connector.Error as err:
                # Manejar errores de conexión
                print("Error de conexión a la base de datos:", err)

        return cls._connection

    @classmethod
    def set_config(cls, config):
        """
        Establece la configuración de la base de datos.

        Args:
            config (dict): Un diccionario con los parámetros de configuración, que incluye:
                - DATABASE_HOST: Dirección del host de la base de datos.
                - DATABASE_USERNAME: Usuario de la base de datos.
                - DATABASE_PASSWORD: Contraseña del usuario.
                - DATABASE_NAME: Nombre de la base de datos.
        """
        cls._config = config

    @classmethod
    def execute_query(cls, query, database_name=None, params=None):
        """
        Ejecuta una consulta SQL que modifica la base de datos (e.g., INSERT, UPDATE, DELETE).

        Args:
            query (str): La consulta SQL a ejecutar.
            database_name (str, opcional): Nombre de la base de datos (no utilizado actualmente).
            params (tuple, opcional): Parámetros para la consulta.

        Returns:
            cursor: Cursor que contiene información sobre la consulta ejecutada.
        """
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        cls._connection.commit()  # Confirma los cambios en la base de datos

        return cursor

    @classmethod
    def fetch_all(cls, query, database_name=None, params=None):
        """
        Ejecuta una consulta SQL y devuelve todos los resultados (e.g., SELECT con múltiples filas).

        Args:
            query (str): La consulta SQL a ejecutar.
            database_name (str, opcional): Nombre de la base de datos (no utilizado actualmente).
            params (tuple, opcional): Parámetros para la consulta.

        Returns:
            list: Lista de todas las filas devueltas por la consulta.
        """
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    @classmethod
    def fetch_one(cls, query, database_name=None, params=None):
        """
        Ejecuta una consulta SQL y devuelve una sola fila (e.g., SELECT con un único resultado esperado).

        Args:
            query (str): La consulta SQL a ejecutar.
            database_name (str, opcional): Nombre de la base de datos (no utilizado actualmente).
            params (tuple, opcional): Parámetros para la consulta.

        Returns:
            tuple: Una fila devuelta por la consulta.
        """
        cursor = cls.get_connection().cursor()
        cursor.execute(query, params)

        return cursor.fetchone()

    @classmethod
    def close_connection(cls):
        """
        Cierra la conexión activa a la base de datos y la elimina.

        Esto es útil para liberar recursos y evitar conexiones abiertas innecesarias.
        """
        if cls._connection is not None:
            cls._connection.close()  # Cierra la conexión
            cls._connection = None  # Elimina la referencia a la conexión
