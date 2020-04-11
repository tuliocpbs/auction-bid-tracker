import http
import json
import os
import random

from locust import HttpLocust, TaskSet, task, events, between

from utils.logger import logger


class AuctionFlow(TaskSet):

    def on_start(self):
        self.create_user()

    def create_user(self):
        user = f'user{random.randint(0, 1000)}'
        self.client.cookies.set('user', user)
        logger.info(f'Create/Get User {user}')

    def create_bid_on_item(self):
        user = self.client.cookies.get('user')

        item = self.get_random_item()

        return {'user': user, 'item':item, 'value': random.randint(0, 10000)}

    @task(1)
    def create_new_bid(self):
        logger.info('New bid...')
        logger.info(str(self.client.cookies.get('token')))
        bid = self.create_bid_on_item()
        response = self.client.put("/v1/bid",
                                   headers={"Content-Type": "application/json",
                                            "Api-Key": os.environ.get('API_KEY', '')},
                                   json=bid)

        if (response.status_code == http.HTTPStatus.CREATED):
            logger.info('Bid accepted')
        else:
            logger.info('Bid not accepted')

    def get_random_item(self):
        qtd_items = int(os.environ.get('QTD_ITEMS', 10))
        return f'item{random.randint(0,qtd_items-1)}'


class AuctionOnline(HttpLocust):
    task_set = AuctionFlow
    wait_time = between(5, 9)
    host = os.environ.get('LOCUST_HOST', 'http://localhost:5000')
