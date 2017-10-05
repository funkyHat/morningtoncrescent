"""REPL and framework for Mornington Crescent game."""

import csv
import pkgutil
from collections import namedtuple
from io import StringIO
import random
from collections import defaultdict

Station = namedtuple('Station', 'name zones lines postcode')


def postcode_zone(postcode):
    return postcode.split()[0]


def load_csv(name):
    stations = pkgutil.get_data(__name__, f'data/{name}.csv').decode('utf8')
    reader = csv.DictReader(StringIO(stations))
    yield from reader


def load_stations():
    lines = load_lines()
    for row in load_csv('stations'):
        yield Station(
            name=row['Station'],
            zones={int(z) for z in row['Zone'].split(',') if z},
            lines=lines[row['Station']],
            postcode=postcode_zone(row['Postcode']),
        )


def load_lines():
    by_station = defaultdict(set)
    for row in load_csv('lines'):
        line = row['Tube Line']
        for k in ('From Station', 'To Station'):
            station = row[k]
            by_station[station].add(line)
    return by_station


STATIONS = {s.name: s for s in load_stations()}
STATIONS_BY_ZONE = {}

for s in STATIONS.values():
    for zone in s.zones:
        STATIONS_BY_ZONE.setdefault(zone, []).append(s)


_STATIONS_LIST = list(STATIONS.values())


def pick_station():
    return random.choice(_STATIONS_LIST)


GOAL = STATIONS['Mornington Crescent']
