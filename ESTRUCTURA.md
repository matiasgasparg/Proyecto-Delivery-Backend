Delivery-Nono-Backend/
│
├── app/
│   ├── __init__.py          # Inicialización de la app Flask.
│   ├── database.py          # Configuración de la conexión a la base de datos.
│   ├── models/              # Modelos de datos 
│   │   
│   │   ├── cliente.py       # Modelo para Clientes.
│   │   ├── repartidor.py    # Modelo para Repartidores.
│   │   ├── pedido.py        # Modelo para Pedidos.
│   │   └── ...              # Otros modelos.
│   ├── controllers/         # Lógica de negocio y controladores.
│   │   
│   │   ├── cliente_controller.py
│   │   ├── pedido_controller.py
│   │   └── ...              # Otros controladores.
│   ├── routes/              # Rutas de la API.
│   │   
│   │   ├── cliente_routes.py
│   │   ├── pedido_routes.py
│   │   └── ...              # Otras rutas.
│   └── uploads/             # Carpeta para subir imágenes u otros archivos.
├── tests/                   # Carpeta para las pruebas
│   ├── __init__.py          # Inicialización de las pruebas.
│   ├── test_plato.py        # Pruebas para el modelo y controlador de Plato.
│   ├── test_cliente.py      # Pruebas para el modelo y controlador de Cliente.
│   ├── test_repartidor.py   # Pruebas para el modelo y controlador de Repartidor.
│   ├── test_pedido.py       # Pruebas para el modelo y controlador de Pedido.
│   ├── conftest.py          # Configuración y fixtures comunes de pytest.
│   └── test_exceptions.py   # Pruebas para excepciones personalizadas.
├── .env                     # Variables de entorno (configuración sensible como claves o credenciales).
├── config.py                # Configuración de la app Flask.
├── requirements.txt         # Dependencias del proyecto.
├── run.py                   # Punto de entrada para ejecutar la aplicación.
└── README.md                # Documentación básica del proyecto.
