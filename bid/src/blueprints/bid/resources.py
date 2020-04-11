import http
import json
from threading import Lock

from flask import jsonify, request
from flask_restful import Resource, Api
from schematics.exceptions import ModelValidationError

from src.utils.logger import logger
from src.utils.api_key import authorize

from .models import Bid


lock = Lock()
bids = []


class BidsResource(Resource):
    decorators = [authorize]

    def get(self):
        try:
            payload = request.get_json() or dict()

            bids_found = self.get_bids_by_item_or_user(item=payload.get('item', None), user=payload.get('user', None))

            return {'status': 'ok', 'msg': 'bids found', 'data': [i.to_primitive() for i in bids_found]}, http.HTTPStatus.OK

        except Exception as e:
            logger.error(f'Unexpected error {repr(e)}')
            return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    def get_bids_by_item_or_user(self, item, user):

        if item and user:
            return [bid for bid in bids if bid.item == item and bid.user == user]
        elif item:
            return [bid for bid in bids if bid.item == item]
        elif user:
            return [bid for bid in bids if bid.user == user]
        else:
            return bids


class BidResource(Resource):
    decorators = [authorize]

    def get(self):
        try:
            payload = request.get_json()

            index, bid = self.get_bid_by_item_and_user(item=payload['item'], user=payload['user'])

            if bid:
                return {'status': 'ok', 'msg': 'bid found', 'data': bid.to_primitive()}, http.HTTPStatus.OK
            else:
                return {'status': 'error', 'msg': 'bid not found', 'data': None}, http.HTTPStatus.NOT_FOUND

        except KeyError:
            logger.error(f'error {repr(e)}')
            return {'status': 'error', 'msg': 'Miss item or user on payload'}, http.HTTPStatus.BAD_REQUEST

        except Exception as e:
            logger.error(f'Unexpected error {repr(e)}')
            return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    def delete(self):
        try:
            payload = request.get_json()

            lock.acquire()

            index, bid = self.get_bid_by_item_and_user(item=payload['item'], user=payload['user'])

            if bid:
                del bids[index]
                lock.release()
                return {'status': 'ok', 'msg': 'bid deleted'}, http.HTTPStatus.OK
            else:
                lock.release()
                return {'status': 'error', 'msg': 'bid not found'}, http.HTTPStatus.NOT_FOUND

        except KeyError:
            logger.error(f'error {repr(e)}')
            return {'status': 'error', 'msg': 'Miss item or user on payload'}, http.HTTPStatus.BAD_REQUEST

        except Exception as e:
            logger.error(f'Unexpected error {repr(e)}')
            return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    def put(self):
        try:
            payload = request.get_json()
            payload.update({'id': len(bids)})

            bid = Bid(payload)
            bid.validate()

            lock.acquire()

            index, exists = self.get_bid_by_item_and_user(item=bid.item, user=bid.user)
            if exists:
                # Update value of bid
                logger.info(f'Bid {bid.id} updated')
                bids[index].value = bid.value
            else:
                # Create new bid
                logger.info(f'Bid {bid.id} created')
                bids.append(bid)
            
            lock.release()
            
            return {'status': 'ok', 'msg': 'Bid created/updated'}, http.HTTPStatus.CREATED

        except ModelValidationError as e:
            logger.error(f'Error in payload validation: {repr(e)}')
            return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.BAD_REQUEST
        
        except Exception as e:
            logger.error(f'Unexpected error {repr(e)}')
            return {'status': 'error', 'msg': repr(e)}, http.HTTPStatus.INTERNAL_SERVER_ERROR

    def get_bid_by_item_and_user(self, item, user):
        for index, bid in enumerate(bids):
            if bid.item == item and bid.user == user:
                logger.info(f'Bid {bid.id} found')
                return index, bid

        return None, None
