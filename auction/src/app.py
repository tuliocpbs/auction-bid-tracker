import os

from elasticapm.contrib.flask import ElasticAPM
from flask import Flask
from flask_cors import CORS

from src.blueprints import healthcheck, swagger, auction


app = Flask(__name__)
CORS(app)

apm = ElasticAPM(app)

healthcheck.init_app(app)
swagger.init_app(app)
auction.init_app(app)
