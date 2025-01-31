import pytest
from app import init_app
from app.database import DatabaseConnection
from app.models.pedido_model import Pedido
from app.controllers.pedido_controller import PedidoController
import datetime
import os
from dotenv import load_dotenv
import mysql.connector
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), "../.env.test")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    print(f"Archivo .env.test cargado desde: {dotenv_path}")
else:
    raise FileNotFoundError(f"El archivo .env.test no se encontró en: {dotenv_path}")

def pytest_configure():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env.test')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        print(f"Archivo .env.test cargado correctamente desde {dotenv_path}")
    else:
        raise FileNotFoundError(f"El archivo {dotenv_path} no se encontró.")
def test_env_cargado():
    from dotenv import dotenv_values
    env = dotenv_values(".env.test")  
    print("Variables cargadas:", env)
    assert "DATABASE_NAME" in env, "DATABASE_NAME no está definido en .env.test"
    assert env["DATABASE_NAME"] == "nono_test", "El valor de DATABASE_NAME no coincide"
     
def test_configuracion_correcta():
    print("DATABASE_NAME cargado:", os.getenv('DATABASE_NAME'))
    assert os.getenv('DATABASE_NAME') == 'nono_test'
@pytest.fixture
def app():
    app = init_app()  # Inicializa la app
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
@pytest.fixture(scope="function", autouse=True)
def setup_and_cleanup():
    # Configura la conexión con la base de datos usando las variables de entorno
    db_config = {
        "DATABASE_HOST": os.getenv("DATABASE_HOST"),
        "DATABASE_USERNAME": os.getenv("DATABASE_USERNAME"),
        "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "DATABASE_NAME": os.getenv("DATABASE_NAME"),
    }
    DatabaseConnection.set_config(db_config)

    try:
        # Intenta obtener la conexión para verificar que es válida
        conn = DatabaseConnection.get_connection()
        assert conn.is_connected(), "No se pudo establecer conexión con la base de datos de prueba"
    finally:
        # Limpieza al final de la prueba
        if DatabaseConnection._connection:
            DatabaseConnection._connection.close()
            DatabaseConnection._connection = None

# Test para obtener los pedidos
def test_get_pedidos(client):
    # Act: Realiza una solicitud GET para obtener los pedidos
    response = client.get('/pedidos/')

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

    # Diagnóstico: Verifica que la respuesta no sea 500 (errores de servidor)
    print(response.data)  # Ver el cuerpo de la respuesta para obtener detalles del error

    # Assert: Verifica que la creación haya sido exitosa
    assert response.status_code == 201
    assert response.json['message'] == 'Pedido creado exitosamente'
