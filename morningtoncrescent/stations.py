"""REPL and framework for Mornington Crescent game."""

import csv
import pkgutil
from collections import namedtuple
from io import StringIO


Station = namedtuple('Station', 'name zone postcode')


def postcode_zone(postcode):
    return postcode.split()[0]


def load_csv(name):
    stations = pkgutil.get_data(__name__, f'data/{name}.csv').decode('utf8')
    reader = csv.DictReader(StringIO(stations))
    for row in reader:

        yield Station(
            name=row['Station'],
            zone={int(z) for z in row['Zone'].split(',') if z},
            postcode=postcode_zone(row['Postcode']),
        )


STATIONS = list(load_csv('stations'))
