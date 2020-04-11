from flask import Blueprint
from flask_restful import Api

from .resources import BidResource, BidsResource


bp = Blueprint("restapi", __name__, url_prefix="/v1")
api = Api(bp)


def init_app(app):
    api.add_resource(BidResource, "/bid")
    api.add_resource(BidsResource, "/bids")
    app.register_blueprint(bp)
