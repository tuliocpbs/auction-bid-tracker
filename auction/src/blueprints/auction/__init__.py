from flask import Blueprint

from .views import get_all_bids_of_item, get_currently_winning_by_item, get_items_with_bids_user


bp = Blueprint('Auction Blueprint', __name__, url_prefix="/api/v1")
bp.add_url_rule('/bidsofanitem', view_func=get_all_bids_of_item, methods=['GET'])
bp.add_url_rule('/currentlywinnig', view_func=get_currently_winning_by_item, methods=['GET'])
bp.add_url_rule('/itemswithuserbids', view_func=get_items_with_bids_user, methods=['GET'])


def init_app(app):
    app.register_blueprint(bp)
