import mysql.connector

class DatabaseConnection:
    """
    Clase para gestionar la conexión a una base de datos MySQL utilizando el patrón Singleton.
    Permite ejecutar consultas y manejar la conexión de manera centralizada.
    """

    _connection = None
    _config = None

    @classmethod
    def get_connection(cls):
        """
        Obtiene la conexión única a la base de datos. Si no existe una conexión, la crea.
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
                print("Error de conexión a la base de datos:", err)
                raise
        return cls._connection

    @classmethod
    def set_config(cls, config):
        """
        Establece la configuración de la base de datos.
        """
        cls._config = config

    @classmethod
    def close_connection(cls):
        """
        Cierra la conexión activa a la base de datos y la elimina.
        """
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None

    # Métodos de ejecución de consultas (insertar, actualizar, etc.) siguen siendo los mismos...
