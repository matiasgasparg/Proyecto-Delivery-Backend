from flask import Blueprint
from ..controllers.pedidodetalle_controller import PedidoDetalleController

pedidodetalle_bp = Blueprint('pedidodetalle_bp', __name__)


pedidodetalle_bp.route('/<int:id_pedido_detalle>', methods=['GET'])(PedidoDetalleController.get)
pedidodetalle_bp.route('/crear', methods=['POST'])(PedidoDetalleController.create)
pedidodetalle_bp.route('/<int:id_pedido_detalle>', methods=['DELETE'])(PedidoDetalleController.delete)
