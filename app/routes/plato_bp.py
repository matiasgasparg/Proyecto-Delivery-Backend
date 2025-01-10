from flask import Blueprint
from ..controllers.plato_controller import PlatoController

# Crear un Blueprint para las rutas relacionadas con platos
plato_bp = Blueprint('plato_bp', __name__)

# Ruta para obtener todos los platos
plato_bp.route('/', methods=['GET'])(PlatoController.get_all)

# Ruta para obtener un plato específico por su ID
plato_bp.route('/<int:id_plato>', methods=['GET'])(PlatoController.get)

# Ruta para crear un nuevo plato
plato_bp.route('/crear', methods=['POST'])(PlatoController.create)

# Ruta para actualizar un plato por su ID
plato_bp.route('/<int:id_plato>', methods=['PUT'])(PlatoController.update)

# Ruta para eliminar un plato por su ID
plato_bp.route('/<int:id_plato>', methods=['DELETE'])(PlatoController.delete)
