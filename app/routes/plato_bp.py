from flask import Blueprint
from ..controllers.plato_controller import PlatoController

plato_bp = Blueprint('plato_bp', __name__)

plato_bp.route('/', methods=['GET'])(PlatoController.get_all)
plato_bp.route('/<int:id_plato>', methods=['GET'])(PlatoController.get)
plato_bp.route('/crear', methods=['POST'])(PlatoController.create)
plato_bp.route('/<int:id_plato>', methods=['PUT'])(PlatoController.update)
plato_bp.route('/<int:id_plato>', methods=['DELETE'])(PlatoController.delete)
