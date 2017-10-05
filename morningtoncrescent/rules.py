
import random as rand
import re
from functools import wraps

from .stations import STATIONS

rules = {}


class InvalidMove(Exception):
    pass


def rule(func):
    name = func.__name__

    if name in rules:
        raise ValueError("Rule {} already exists".format(name))
    rules[name] = func

    return func


def simple_rule(func):

    @rule
    @wraps(func)
    def wrapper(stations):
        if len(stations) < 2:
            return
        return func(*stations[-2:])

    return wrapper


@rule
def random(stations):
    valid = rand.sample(STATIONS.keys(), 20)

    if stations[-1] not in valid:
        raise InvalidMove('Not allowed')


@simple_rule
def one_zone_each_turn(previous, next):
    for zone in previous.zones:

        if not any(
                -1 <= next_zone - zone <= 1
                for next_zone in next.zones):
            raise InvalidMove("Can't move from zone {} to zone {}".format(
                previous.zones, next.zones))


@simple_rule
def arbitrary_horrible_postcode_rule(previous, next):
    prev_number, next_number = (
            int(re.search('\d+', station.postcode).group(0))
            for station
            in (previous, next))
    if not -5 <= prev_number - next_number <= 5:
        raise InvalidMove(
                "Can't move from postcode {} to postcode {}".format(
                    previous.postcode, next.postcode))
