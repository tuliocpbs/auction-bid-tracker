import requests

from src.config.api_key import ApiKeySettings
from src.utils.logger import logger

from .exceptions import ErrorGetInfoBidApi


class Bid:

    @classmethod
    def get_bids(cls, item=None, user=None):
        apikey = ApiKeySettings()
        body = cls.create_payload(item, user)

        try:
            resp = requests.get("http://localhost:5001/v1/bid",
                                headers={"Content-Type": "application/json",
                                        "Api-Key": apikey.API_KEY},
                                json=body,
                                timeout=30)

            if not resp.ok:
                logger.error(f'Error getting info from Bid API, response status code {resp.status_code}')
                raise(ErrorGetInfoBidApi)

            bids = resp.json().get('data', [])
            logger.info(f'Get {len(bids)} bids from Bid API')
            return bids
        
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout, ErrorGetInfoBidApi) as e:
            logger.error(f'Connection error {repr(e)}')
            return []

    @classmethod
    def create_payload(cls, item, user):
        if item and user:
            return {'item':item, 'user':user}
        elif item:
            return {'item': item}
        elif user:
            return {'user': user}
        else:
            return dict()
