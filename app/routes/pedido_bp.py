from flask import Blueprint
from ..controllers.pedido_controller import PedidoController

pedido_bp = Blueprint('pedido_bp', __name__)

pedido_bp.route('/', methods=['GET'])(PedidoController.get_all)
pedido_bp.route('/<int:id_pedido>', methods=['GET'])(PedidoController.get)
pedido_bp.route('/crear', methods=['POST'])(PedidoController.create)
pedido_bp.route('/<int:id_pedido>', methods=['PUT'])(PedidoController.update)
pedido_bp.route('/<int:id_pedido>', methods=['DELETE'])(PedidoController.delete)

pedido_bp.route('/<int:id_pedido>/modify-platos', methods=['PUT'])(PedidoController.modify_platos)
