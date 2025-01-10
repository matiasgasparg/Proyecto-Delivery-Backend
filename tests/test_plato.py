import pytest
from app import DatabaseConnection

def test_create_plato(client):
    # Insertar un plato
    response = client.post('/platos', json={
        "nombre": "Pizza",
        "descripcion": "Pizza de mozzarella",
        "precio": 500,
        "disponible": True
    })

    # Verificar respuesta HTTP
    assert response.status_code == 201

    # Verificar en la base de datos
    platos = DatabaseConnection.fetch_all("SELECT * FROM platos WHERE nombre = %s", params=("Pizza",))
    assert len(platos) == 1
    assert platos[0][1] == "Pizza"  # Dependiendo del orden de las columnas
@pytest.fixture(autouse=True)
def clean_database():
    yield
    DatabaseConnection.execute_query("DELETE FROM platos")
    # Repite para otras tablas según sea necesario
