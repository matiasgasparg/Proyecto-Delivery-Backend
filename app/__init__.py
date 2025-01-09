from flask import Flask
from flask_cors import CORS
from config import Config

from .routes.plato_bp import plato_bp

from .routes.error_handlers import errors

from .database import DatabaseConnection

def init_app():
    """Crea y configura la aplicación Flask"""
    
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)
    app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se guardarán las imágenes

    CORS(app, supports_credentials=True)

    app.config.from_object(
        Config
    )

    DatabaseConnection.set_config(app.config)

    app.register_blueprint(plato_bp, url_prefix = '/platos')


    app.register_blueprint(errors)

    return app