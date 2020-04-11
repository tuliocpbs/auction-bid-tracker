import http

from flask import jsonify, request

from src.utils.logger import logger
from src.utils.api_key import authorize

from src.blueprints.bid.resources import bids


def get_currently_winning_by_item():
    try:
        payload = request.get_json()

        bids_of_item = [bid for bid in bids if bid.item == payload.get('item', None)]

        bids_of_item_ordered = sorted(bids_of_item, key=lambda x: x.value, reverse=True)

        return {'status': 'ok', 'msg': 'currently winning', 'data': bids_of_item_ordered[0].user}, http.HTTPStatus.OK

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR


def get_all_bids_of_item():
    try:
        payload = request.get_json()
    
        bids_of_item = [bid for bid in bids if bid.item == payload.get('item', None)]

        return {'status': 'ok', 'msg': 'bids found', 'data': [i.to_primitive() for i in bids_of_item]}, http.HTTPStatus.OK

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR


def get_items_with_bids_user():
    try:
        payload = request.get_json()

        bids_of_user = [bid for bid in bids if bid.user == payload.get('user', None)]

        return {'status': 'ok', 'msg': 'items found', 'data': [i.item for i in bids_of_user]}, http.HTTPStatus.OK

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR
