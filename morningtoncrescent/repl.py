import readline
from functools import lru_cache

from .stations import STATIONS, GOAL, pick_station
from .rules import rules, InvalidMove


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
    history = []
    while True:
        cpu_pick = pick_station()
        print(f'{cpu_pick.name}!')

        if cpu_pick == GOAL:
            print('I win!')
            return
        history.append(cpu_pick)

        while True:
            human_pick = input("Your move? ")
            try:
                station = STATIONS[human_pick]
            except KeyError:
                continue

            try:
                for rule in rules.values():
                    rule(history + [station])
            except InvalidMove as e:
                print(e.args[0])
                continue
            else:
                break

        print()

        if station == GOAL:
            print('Drat, great move!')
            return

        history.append(station)
