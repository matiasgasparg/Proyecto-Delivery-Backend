Delivery-Nono-Backend/
│
├── app/
│   ├── __init__.py          # Inicialización de la app Flask.
│   ├── database.py          # Configuración de la conexión a la base de datos.
│   ├── models/              # Modelos de datos (ORM o SQLAlchemy).
│   │   ├── __init__.py
│   │   ├── cliente.py       # Modelo para Clientes.
│   │   ├── repartidor.py    # Modelo para Repartidores.
│   │   ├── pedido.py        # Modelo para Pedidos.
│   │   └── ...              # Otros modelos.
│   ├── controllers/         # Lógica de negocio y controladores.
│   │   ├── __init__.py
│   │   ├── cliente_controller.py
│   │   ├── pedido_controller.py
│   │   └── ...              # Otros controladores.
│   ├── routes/              # Rutas de la API.
│   │   ├── __init__.py
│   │   ├── cliente_routes.py
│   │   ├── pedido_routes.py
│   │   └── ...              # Otras rutas.
│   └── uploads/             # Carpeta para subir imágenes u otros archivos.
│
├── .env                     # Variables de entorno (configuración sensible como claves o credenciales).
├── config.py                # Configuración de la app Flask.
├── requirements.txt         # Dependencias del proyecto.
├── run.py                   # Punto de entrada para ejecutar la aplicación.
└── README.md                # Documentación básica del proyecto.
