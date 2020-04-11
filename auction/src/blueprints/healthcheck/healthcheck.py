import http
from flask import jsonify


def healthcheck():
    return jsonify({'status': "green"}), http.HTTPStatus.OK
