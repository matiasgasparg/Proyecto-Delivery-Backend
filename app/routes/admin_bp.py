from flask import Blueprint
from ..controllers.admin_controller import AdminController

admin_bp = Blueprint('admin_bp', __name__)

admin_bp.route('/login', methods=['POST'])(AdminController.login)
admin_bp.route('/crear', methods=['POST'])(AdminController.create)
