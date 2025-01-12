from flask import Blueprint
from ..controllers.opinion_controller import OpinionController

opinion_bp = Blueprint('opinion_bp', __name__)

opinion_bp.route('/<int:id_opinion>', methods=['GET'])(OpinionController.get)
opinion_bp.route('/crear', methods=['POST'])(OpinionController.create)
opinion_bp.route('/<int:id_opinion>', methods=['DELETE'])(OpinionController.delete)
