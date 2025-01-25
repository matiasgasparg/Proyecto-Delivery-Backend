from flask import Blueprint
from ..controllers.repartidor_controller import RepartidorController

repartidor_bp = Blueprint('repartidor_bp', __name__)

repartidor_bp.route('/', methods=['GET'])(RepartidorController.get_all)
repartidor_bp.route('/<int:id_repartidor>', methods=['GET'])(RepartidorController.get)
repartidor_bp.route('/crear', methods=['POST'])(RepartidorController.create)
repartidor_bp.route('/<int:id_repartidor>', methods=['PUT'])(RepartidorController.update)
repartidor_bp.route('/<int:id_repartidor>', methods=['DELETE'])(RepartidorController.delete)

# Nueva ruta para filtrar repartidores disponibles
repartidor_bp.route('/disponibles', methods=['GET'])(RepartidorController.get_available)
repartidor_bp.route('/login', methods=['POST'])(RepartidorController.login)
