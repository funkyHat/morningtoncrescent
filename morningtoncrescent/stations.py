"""REPL and framework for Mornington Crescent game."""

import csv
import pkgutil
from collections import namedtuple
from io import StringIO


Station = namedtuple('Station', 'name zones postcode')


def postcode_zone(postcode):
    return postcode.split()[0]


def load_csv(name):
    stations = pkgutil.get_data(__name__, f'data/{name}.csv').decode('utf8')
    reader = csv.DictReader(StringIO(stations))
    for row in reader:
        yield Station(
            name=row['Station'],
            zones={int(z) for z in row['Zone'].split(',') if z},
            postcode=postcode_zone(row['Postcode']),
        )


STATIONS = {s.name: s for s in load_csv('stations')}
STATIONS_BY_ZONE = {}

for s in STATIONS.values():
    for zone in s.zones:
        STATIONS_BY_ZONE.setdefault(zone, []).append(s)
