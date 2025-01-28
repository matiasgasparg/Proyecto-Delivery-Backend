import pytest
from app import init_app
from app.database import DatabaseConnection  # Corregir importación de DatabaseConnection
from app.models.pedido_model import Pedido
from app.controllers.pedido_controller import PedidoController
import datetime

# Fixture para la inicialización de la aplicación y base de datos
@pytest.fixture(scope="module")
def app():
    """
    Inicializa la aplicación Flask una sola vez para todas las pruebas en el módulo.
    """
    app = init_app()  # Inicializa la aplicación Flask
    DatabaseConnection.set_config(app.config)  # Configura la conexión a la base de datos
    yield app  # Esta es la instancia de la app que se pasa a las pruebas
    # Aquí puedes agregar limpieza, si es necesario, después de todas las pruebas

# Fixture para el cliente de la aplicación
@pytest.fixture
def client(app):
    """
    Proporciona un test client para simular solicitudes HTTP.
    """
    return app.test_client()

# Fixture para el controlador de pedidos
@pytest.fixture
def pedido_controller(app):
    return PedidoController(app)  # Usamos la app ya configurada

# Fixture para la configuración y limpieza de la base de datos antes y después de las pruebas
@pytest.fixture(autouse=True)
def setup(app):  # Cambié 'config' a 'app' porque 'app' es el objeto de la aplicación Flask
    # Configura la base de datos con la configuración de Flask
    DatabaseConnection.set_config(app.config)

    # Realiza las configuraciones necesarias antes de cada prueba
    with DatabaseConnection.get_connection() as conn:
        cursor = conn.cursor()

        # Asegúrate de que la conexión se haya establecido antes de ejecutar el script
        if conn.is_connected():
            print("Conexión exitosa a la base de datos.")
        else:
            print("Error en la conexión a la base de datos.")

        # Ejecutar el script SQL de inicialización
        with open("nono_test.sql", "r") as file:
            sql_script = file.read()

        sql_statements = sql_script.split(";")
        for statement in sql_statements:
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        cursor.close()

    yield

    # Limpieza después de las pruebas
    with DatabaseConnection.get_connection() as conn:
        cleanup(conn)

# Función de limpieza para después de las pruebas
def cleanup(conn):
    cursor = conn.cursor()
    # Ejecutar sentencias SQL de limpieza
    cursor.execute("DELETE FROM pedido WHERE id_cliente = 1")  # Ejemplo de limpieza
    conn.commit()
    cursor.close()


# Test para crear un nuevo pedido
def test_create_pedido(client):  # Usamos el fixture 'client' en lugar de crear el cliente aquí
    # Arrange
    nuevo_pedido = {
        "id_cliente": 1,
        "id_repartidor": 1,
        "domicilio_entrega": "Calle Falsa 123",
        "estado": "pendiente",
        "fecha_hora": datetime.datetime.now().isoformat(),
        "comentario": "Pedido urgente",
        "platos": [
            {"id_plato": 1, "cantidad": 2, "comentario": "Sin sal"}
        ]
    }

    # Act
    response = client.post('/pedidos/crear', json=nuevo_pedido)  # Ajusta la ruta aquí

    # Assert
    assert response.status_code == 201
    assert response.json['message'] == 'Pedido creado exitosamente'
