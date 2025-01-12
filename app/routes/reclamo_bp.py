from flask import Blueprint
from ..controllers.reclamo_controller import ReclamoController

reclamo_bp = Blueprint('reclamo_bp', __name__)


reclamo_bp.route('/<int:id_reclamo>', methods=['GET'])(ReclamoController.get)
reclamo_bp.route('/crear', methods=['POST'])(ReclamoController.create)
reclamo_bp.route('/<int:id_reclamo>', methods=['DELETE'])(ReclamoController.delete)
