from flask import Flask
from flask_cors import CORS
from config import Config

from .routes.plato_bp import plato_bp
from .routes.cliente_bp import cliente_bp
from .routes.repartidor_bp import repartidor_bp
from .routes.promocion_bp import promocion_bp
from .routes.pedido_bp import pedido_bp
from .routes.pedidodetalle_bp import pedidodetalle_bp
from .routes.reclamo_bp import reclamo_bp
from .routes.opinion_bp import opinion_bp
from .routes.error_handlers import errors
from .routes.admin_bp import admin_bp

from .database import DatabaseConnection

def init_app():
    """
    Crea y configura la aplicación Flask.

    Configura los valores básicos de la aplicación, inicializa la conexión a la base de datos,
    habilita el soporte para CORS y registra los Blueprints para manejar las rutas y los errores.

    Returns:
        Flask: Instancia configurada de la aplicación Flask.
    """
    
    # Crear una instancia de Flask con las carpetas estática y de plantillas definidas en la configuración.
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)
    
    # Configuración para la carpeta donde se guardarán las imágenes cargadas por los usuarios.
    app.config['UPLOAD_FOLDER'] = 'uploads'

    # Habilitar Cross-Origin Resource Sharing (CORS) para permitir solicitudes desde diferentes orígenes.
    CORS(app, supports_credentials=True)

    # Cargar la configuración desde el objeto Config definido en el módulo `config`.
    app.config.from_object(Config)

    # Configurar la conexión a la base de datos utilizando los parámetros definidos en la configuración.
    DatabaseConnection.set_config(app.config)

    # Registrar los Blueprints de las rutas relacionadas con las diferentes entidades.
    app.register_blueprint(plato_bp, url_prefix='/platos')
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(repartidor_bp, url_prefix='/repartidores')
    app.register_blueprint(promocion_bp, url_prefix='/promociones')
    app.register_blueprint(pedido_bp, url_prefix='/pedidos')
    app.register_blueprint(pedidodetalle_bp, url_prefix='/pedidos-detalle')
    app.register_blueprint(reclamo_bp, url_prefix='/reclamos')
    app.register_blueprint(opinion_bp, url_prefix='/opiniones')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Registrar el Blueprint para el manejo centralizado de errores personalizados.
    app.register_blueprint(errors)

    # Devolver la instancia configurada de Flask.
    return app
