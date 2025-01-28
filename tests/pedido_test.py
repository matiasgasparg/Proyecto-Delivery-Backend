import pytest
from app import init_app
from app.database import DatabaseConnection
from app.models.pedido_model import Pedido
from app.controllers.pedido_controller import PedidoController
import datetime
from dotenv import load_dotenv
import mysql.connector

# Cargar variables de entorno antes de las pruebas

def pytest_configure():
    load_dotenv()  # Esto asegura que las variables de entorno se carguen antes de las pruebas

# Fixture para la inicialización de la aplicación y base de datos
@pytest.fixture
def app():
    app = init_app()  # Esta es la instancia de tu aplicación
    yield app
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
def setup(app):
    DatabaseConnection.set_config(app.config)
    try:
        conn = DatabaseConnection.get_connection()
        cursor = conn.cursor()
        
        # Consumir resultados pendientes si los hay
        while cursor.nextset():  # Consume todos los conjuntos de resultados pendientes
            pass
        
        cursor.execute("SELECT 1")  # Hacer una consulta simple para verificar la conexión
        conn.commit()
        print("Conexión exitosa a la base de datos.")
    except mysql.connector.errors.OperationalError as e:
        pytest.fail(f"Error de conexión a la base de datos: {e}")
    yield

# Limpieza de datos de prueba
def cleanup(conn):
    cursor = conn.cursor()
    # Realiza limpieza específica
    cursor.execute("DELETE FROM pedido WHERE id_cliente = 1")  # Ejemplo de limpieza
    conn.commit()
    cursor.close()

# Test para obtener los pedidos
def test_get_pedidos(client):
    # Act: Realiza una solicitud GET para obtener los pedidos
    response = client.get('pedidos/')

    # Assert: Verifica que la respuesta sea exitosa
    assert response.status_code == 200
    # Verifica que la respuesta contenga datos, si es que hay pedidos en la base de datos
    assert isinstance(response.json, list)

# Test para crear un nuevo pedido
def test_create_pedido(client):
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

    # Act: Simula la solicitud POST para crear un pedido
    response = client.post('/pedidos/crear', json=nuevo_pedido)

    # Assert: Verifica que la creación haya sido exitosa
    assert response.status_code == 201
    assert response.json['message'] == 'Pedido creado exitosamente'
