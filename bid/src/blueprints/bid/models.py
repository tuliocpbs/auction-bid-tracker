from schematics.models import Model
from schematics.types import StringType, IntType
from schematics.exceptions import ValidationError


class Bid(Model):
    id = IntType(required=True)
    user = StringType(required=True)
    item = StringType(required=True)
    value = IntType(required=True)
    