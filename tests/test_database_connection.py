import pytest
from unittest.mock import patch, MagicMock
from database import DatabaseConnection  # Asegúrate de que esta clase se ajuste a tus pruebas.
from mysql.connector.errors import IntegrityError, DataError
import datetime

# Fixture para la configuración de la base de datos de pruebas
@pytest.fixture
def config():
    """
    Devuelve un diccionario con los parámetros de configuración de la base de datos 
    para la prueba, como el host, usuario, contraseña y nombre de la base de datos.
    """
    return {
        'DATABASE_HOST': 'localhost',
        'DATABASE_USERNAME': 'test_user',
        'DATABASE_PASSWORD': 'test_password',
        'DATABASE_NAME': 'test_db'
    }

# Configura la base de datos al establecer la configuración de conexión
DatabaseConnection.set_config(config)


# Fixture para la configuración y limpieza de la base de datos
@pytest.fixture
def setup_db(config):
    """
    Establece la configuración de la base de datos antes de cada prueba 
    y limpia la base de datos después de cada prueba.
    """
    DatabaseConnection.set_config(config)

    # Limpieza de la base de datos después de cada prueba
    yield

    # Aquí se puede agregar código para limpiar la base de datos si es necesario.


def test_get_connection(config):
    """
    Verifica que la conexión a la base de datos sea creada correctamente utilizando los parámetros configurados.
    """
    DatabaseConnection.set_config(config)
    
    # Usar un mock para interceptar la creación de la conexión
    with patch('mysql.connector.connect') as mock_connect:
        mock_connect.return_value = MagicMock()  # Mock de la conexión
        connection = DatabaseConnection.get_connection()

        # Verificar que la función connect fue llamada con los parámetros correctos
        mock_connect.assert_called_once_with(
            host=config['DATABASE_HOST'],
            user=config['DATABASE_USERNAME'],
            password=config['DATABASE_PASSWORD'],
            database=config['DATABASE_NAME']
        )
        
        # Verificar que la conexión no es None
        assert connection is not None


def test_fetch_all(config, setup_db):
    """
    Verifica que el método fetch_all ejecute una consulta correctamente 
    y devuelva los resultados esperados utilizando un mock para la conexión y el cursor.
    """
    query = "SELECT * FROM test_table"

    # Mock de la conexión y el cursor
    with patch('database.DatabaseConnection.get_connection') as mock_get_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Simula el comportamiento de fetchall
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]  # Simulación de resultados
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection  # Mock de la conexión

        # Llamada al método fetch_all que estamos probando
        results = DatabaseConnection.fetch_all(query)

        # Verificar que execute fue llamado correctamente con los parámetros esperados
        mock_cursor.execute.assert_called_once_with(query, None)
        
        # Verificar que los resultados se retornaron correctamente
        assert results == [('row1',), ('row2',)]


def test_fetch_one(config, setup_db):
    """
    Verifica que el método fetch_one ejecute una consulta correctamente 
    y devuelva el resultado esperado utilizando un mock para la conexión y el cursor.
    """
    query = "SELECT * FROM test_table WHERE id = 1"

    # Mock de la conexión y el cursor
    with patch('database.DatabaseConnection.get_connection') as mock_get_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Simula el comportamiento de fetchone
        mock_cursor.fetchone.return_value = ('row1',)  # Simulación de un solo resultado
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection  # Mock de la conexión

        # Llamada al método fetch_one que estamos probando
        result = DatabaseConnection.fetch_one(query)

        # Verificar que execute fue llamado correctamente con los parámetros esperados
        mock_cursor.execute.assert_called_once_with(query, None)
        
        # Verificar que el resultado sea el esperado
        assert result == ('row1',)


def test_insert(config, setup_db):
    """
    Verifica que el método insert inserte correctamente los datos en la base de datos.
    """
    query = "INSERT INTO test_table (name, age) VALUES (%s, %s)"
    data = ("John Doe", 30)

    # Mock de la conexión y el cursor
    with patch('database.DatabaseConnection.get_connection') as mock_get_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Simula el comportamiento de ejecutar una consulta
        mock_cursor.lastrowid = 1  # Simula que el último id insertado es 1
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection  # Mock de la conexión

        # Llamada al método insert que estamos probando
        result = DatabaseConnection.insert(query, data)

        # Verificar que execute fue llamado correctamente con los parámetros esperados
        mock_cursor.execute.assert_called_once_with(query, data)
        
        # Verificar que el id de la última fila insertada es el esperado
        assert result == 1


def test_update(config, setup_db):
    """
    Verifica que el método update actualice correctamente los datos en la base de datos.
    """
    query = "UPDATE test_table SET name = %s WHERE id = %s"
    data = ("Updated Name", 1)

    # Mock de la conexión y el cursor
    with patch('database.DatabaseConnection.get_connection') as mock_get_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        # Simula el comportamiento de ejecutar una consulta
        mock_cursor.rowcount = 1  # Simula que se actualizó una fila
        mock_connection.cursor.return_value = mock_cursor
        mock_get_connection.return_value = mock_connection  # Mock de la conexión

        # Llamada al método update que estamos probando
        result = DatabaseConnection.update(query, data)

        # Verificar que execute fue llamado correctamente con los parámetros esperados
        mock_cursor.execute.assert_called_once_with(query, data)
        
        # Verificar que se actualizó una fila
        assert result == 1
