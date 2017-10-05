import readline
from functools import lru_cache

from .stations import STATIONS


@lru_cache()
def complete(text):
    text = text.lower()
    return [s for s in STATIONS if s.lower().startswith(text)]


def station_completer(text, state):
    try:
        return complete(text)[state]
    except IndexError:
        return None


def station_exists(station):
    return station in STATIONS.keys()


readline.parse_and_bind("tab: complete")
readline.set_completer(station_completer)


def repl():
    while True:
        station = input("Your move? ")
        print(station_exists(station))
