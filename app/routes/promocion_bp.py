from flask import Blueprint
from ..controllers.promocion_controller import PromocionController

promocion_bp = Blueprint('promocion_bp', __name__)

promocion_bp.route('/', methods=['GET'])(PromocionController.get_all)
promocion_bp.route('/crear', methods=['POST'])(PromocionController.create)
