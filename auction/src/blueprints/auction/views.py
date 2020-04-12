import http

from flask import jsonify, request

from src.utils.logger import logger
from src.utils.api_key import authorize

from src.repositories.bid import Bid

@authorize
def get_currently_winning_by_item():
    try:
        item = request.args.get('item', None)

        bids_of_item = Bid.get_bids(item=item)

        bids_of_item_ordered = sorted(bids_of_item, key=lambda x: x['value'], reverse=True)

        return {'status': 'ok', 'msg': 'currently winning', 'data': bids_of_item_ordered[0].get('user', None)}, http.HTTPStatus.OK

    except IndexError as e:
        logger.error(f'Item {item} not found')
        return {'status': 'ok', 'msg': 'item not found', 'data': None}, http.HTTPStatus.NOT_FOUND

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e), 'data': None}, http.HTTPStatus.INTERNAL_SERVER_ERROR

@authorize
def get_all_bids_of_item():
    try:
        item = request.args.get('item', None)

        bids_of_item = Bid.get_bids(item=item)

        return {'status': 'ok', 'msg': 'bids found', 'data': bids_of_item}, http.HTTPStatus.OK

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e), 'data': None}, http.HTTPStatus.INTERNAL_SERVER_ERROR

@authorize
def get_items_with_bids_user():
    try:
        user = request.args.get('user', None)

        bids_of_user = Bid.get_bids(user=user)

        return {'status': 'ok', 'msg': 'items found', 'data': [i['item'] for i in bids_of_user]}, http.HTTPStatus.OK

    except Exception as e:
        logger.error(f'Unexpected error {repr(e)}')
        return {'status': 'error', 'msg': repr(e), 'data': None}, http.HTTPStatus.INTERNAL_SERVER_ERROR
