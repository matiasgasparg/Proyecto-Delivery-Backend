from flask import Blueprint
from ..controllers.promocion_controller import PromocionController

promocion_bp = Blueprint('promocion_bp', __name__)

promocion_bp.route('/', methods=['GET'])(PromocionController.get_all)
promocion_bp.route('/<int:id_promocion>', methods=['GET'])(PromocionController.get)
promocion_bp.route('/crear', methods=['POST'])(PromocionController.create)
promocion_bp.route('/<int:id_promocion>', methods=['PUT'])(PromocionController.update)
promocion_bp.route('/<int:id_promocion>', methods=['DELETE'])(PromocionController.delete)
