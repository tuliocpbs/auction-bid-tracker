import pytest
from schematics.exceptions import ModelValidationError

from src.blueprints.bid.models import Bid

def test_valid_bid_model():
    bid = Bid({'id':1, 'user': 'user1', 'item': 'item1', 'value': 1000})
    bid.validate()

    assert True

def test_bid_model_miss_field_id():
    bid = Bid({'user': 'user1', 'item': 'item1', 'value': 1000})

    with pytest.raises(ModelValidationError):
        bid.validate()

def test_bid_model_miss_field_user():
    bid = Bid({'id':1, 'item': 'item1', 'value': 1000})

    with pytest.raises(ModelValidationError):
        bid.validate()

def test_bid_model_miss_field_item():
    bid = Bid({'id':1, 'user': 'user1', 'value': 1000})

    with pytest.raises(ModelValidationError):
        bid.validate()

def test_bid_model_miss_field_value():
    bid = Bid({'id':1, 'user': 'user1', 'item': 'item1'})

    with pytest.raises(ModelValidationError):
        bid.validate()
