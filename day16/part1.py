#!/usr/bin/env python

from collections import defaultdict
from pprint import pprint
from sys import argv, stdin
import re

debug = 'debug' in argv

rates = {}
neighbors = defaultdict(list)
parser = re.compile(
    r'(?P<_id>\w+) has .* rate=(?P<rate>\d+); .* valves? (?P<neighbors>.*)$'
)
for line in stdin:
    match = parser.search(line)
    id = match.group('_id')
    rate = int(match.group('rate'))
    rates[id] = rate
    neigh = match.group('neighbors').split(', ')
    neighbors[id] = neigh

ids = rates.keys()
if debug:
    pprint({'ids': ids, 'rates': rates, 'neighbors': neighbors})

# https://en.wikipedia.org/wiki/Shortest_path_problem
# Floyd–Warshall algorithm https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
dists = defaultdict(lambda: defaultdict(lambda: 9999))
for id, neigh in neighbors.items():
    d = dists[id]
    # we're 0 away from ourself
    d[id] = 0
    # we're 1 away from our neighbors
    for neighbor in neigh:
        d[neighbor] = 1
if debug:
    pprint(dists)

for k in ids:
    for i in ids:
        for j in ids:
            d = dists[i][k] + dists[k][j]
            if dists[i][j] > d:
                dists[i][j] = d
if debug:
    pprint(dists)


# things we can open, exclude anything with a 0 rate since they don't help
candidates = set(id for id, rate in rates.items() if rate > 0)
if debug:
    pprint({'candidates': candidates})


def best_option(current, t=30, pressure=0, prefix=''):
    if debug:
        print(
            f'{prefix}best_option: current={current}, t={t}, pressure={pressure}'
        )

    # if time is almost up (we need 1 to open anything) or there's nothing left
    # to open
    if t == 1 or len(candidates) == 0:
        return pressure

    options = []

    # list makes a copy so we can modify things in the loop
    for candidate in list(candidates):
        # how far away is it
        dist = dists[current][candidate]
        # what will t be once we get there and open it
        after = t - dist - 1
        if after < 0:
            # no point in going there if there's no time left after its open
            continue

        # open it
        candidates.remove(candidate)

        # figure out what it will contribute once on
        contribution = rates[candidate] * after
        # search from there adding anything we've accumilated so far
        score = best_option(
            candidate, after, pressure + contribution, f'{prefix}  '
        )
        options.append((score, candidate))

        # close it
        candidates.add(candidate)

    # order options best to worst
    options.sort(reverse=True)

    if debug:
        print(f'best_option: current={current}, t={t}, pressure={pressure}')
        for score, option in options:
            print(f'  {option} {score}')

    try:
        # return the best option we found
        return options[0][0]
    except IndexError:
        # we didn't find any options, return what we were passed
        return pressure


best = best_option('AA')
print(best)
