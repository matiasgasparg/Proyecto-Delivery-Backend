from flask import Blueprint
from ..controllers.cliente_controller import ClienteController

cliente_bp = Blueprint('cliente_bp', __name__)

cliente_bp.route('/', methods=['GET'])(ClienteController.get_all)
cliente_bp.route('/<int:id_cliente>', methods=['GET'])(ClienteController.get)
cliente_bp.route('/crear', methods=['POST'])(ClienteController.create)
cliente_bp.route('/<int:id_cliente>', methods=['PUT'])(ClienteController.update)
cliente_bp.route('/<int:id_cliente>', methods=['DELETE'])(ClienteController.delete)
cliente_bp.route('/<string:email>', methods=['GET'])(ClienteController.get_by_email)
