from flask import Blueprint
from ..controllers.comboplato_controller import ComboPlatoController

comboplato_bp = Blueprint('comboplato_bp', __name__)

comboplato_bp.route('/', methods=['GET'])(ComboPlatoController.get_all)
comboplato_bp.route('/<int:id_combo_plato>', methods=['GET'])(ComboPlatoController.get)
comboplato_bp.route('/crear', methods=['POST'])(ComboPlatoController.create)
comboplato_bp.route('/<int:id_combo_plato>', methods=['DELETE'])(ComboPlatoController.delete)
