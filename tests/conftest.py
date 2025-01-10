import pytest
from app.database import DatabaseConnection
from app import init_app
from dotenv import load_dotenv
import os

@pytest.fixture
def app():
    """Crea y configura la aplicación Flask para pruebas."""
    # Cargar el archivo .env.test
    load_dotenv(dotenv_path='.env.test')

    app = init_app()
    app.config.update({
        "TESTING": True,
    })

    # Configuración de la base de datos para pruebas (ya se carga desde el .env.test)
    DatabaseConnection.set_config({
        "DATABASE_HOST": os.getenv("DATABASE_HOST"),
        "DATABASE_USERNAME": os.getenv("DATABASE_USERNAME"),
        "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD"),
        "DATABASE_NAME": os.getenv("DATABASE_NAME"),
    })

    # Crear las tablas y datos iniciales necesarios (si corresponde)
    with app.app_context():
        # Aquí podrías agregar scripts para inicializar la base de datos si es necesario
        pass

    yield app

    # Después de las pruebas, limpiar recursos
    DatabaseConnection.close_connection()

@pytest.fixture
def client(app):
    """Crea un cliente de prueba para Flask."""
    return app.test_client()
