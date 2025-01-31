**Delivery Nono:** es una aplicación diseñada para gestionar los pedidos de una rotisería. El sistema incluye funcionalidades para clientes, repartidores y administradores, permitiendo realizar pedidos, gestionarlos y entregarlos de manera eficiente.

## Tecnologías Utilizadas

- **Frontend:** React, Vite, CSS puro.
- **Backend:** Flask (Python).
- **Base de Datos:** MySQL.
- **Almacenamiento de Imágenes:** Firebase Storage.
- **Despliegue:**
  - Frontend: Firebase Hosting.
  - Backend: PythonAnywhe

## Estructura del proyecto

```bash
app/
│   src/
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── admin_model.py
│   │   ├── cliente_model.py
│   │   ├── exceptions.py
│   │   ├── img_model.py
│   │   ├── opinion_model.py
│   │   ├── pedido_model.py
│   │   ├── pedidodetalle_model.py
│   │   ├── plato_model.py
│   │   ├── promocion_model.py
│   │   ├── reclamo_model.py
│   │   ├── repartidor_model.py
│   ├── controllers/
│   │   ├── admin_controller.py
│   │   ├── cliente_controller.py
│   │   ├── img_controller.py
│   │   ├── opinion_controller.py
│   │   ├── pedido_controller.py
│   │   ├── pedidodetalle_controller.py
│   │   ├── pedidopromocion_controller.py
│   │   ├── plato_controller.py
│   │   ├── promocion_controller.py
│   │   ├── reclamo_controller.py
│   │   ├── repartidor_controller.py
│   ├── routes/
│   │   ├── admin_bp.py
│   │   ├── cliente_bp.py
│   │   ├── error_handlers.py
│   │   ├── img_bp.py
│   │   ├── opinion_bp.py
│   │   ├── pedido_bp.py
│   │   ├── pedidodetalle_bp.py
│   │   ├── plato_bp.py
│   │   ├── promocion_bp.py
│   │   ├── reclamo_bp.py
│   │   ├── repartidor_bp.py
├── tests/
│   config.py
│   database.py
│   pedido_test.py
│   test_database_connection.py
```

## Instalación

1. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

2. Crear un archivo `.env` en la raíz del proyecto. El repositorio cuenta con un archivo `.env` que puedes utilizar como base.

3. Crear una base de datos en MySQL y configurar las credenciales en el archivo `.env`.

4. Para lanzar la aplicación, ejecutar el siguiente comando:

```bash
flask --app app run
```
