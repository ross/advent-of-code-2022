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


def best_options(
    current_me, current_elephant, t_me=26, t_elephant=26, pressure=0, prefix=''
):
    if debug:
        print(
            f'{prefix}best_option: current_me={current_me}, current_elephant={current_elephant}, t_me={t_me}, '
            f't_elephant={t_elephant}, pressure={pressure}, candidates={candidates}'
        )

    # if time is almost up (we need 1 to open anything) or there's nothing left
    # to open
    if t_me <= 0 or len(candidates) == 0:
        return pressure

    options = []

    # list makes a copy so we can modify things in the loop
    for candidate_me in list(candidates):
        # how far away is it
        dist_me = dists[current_me][candidate_me]

        # what will t be once we get there and open it
        after_me = t_me - dist_me - 1

        # note that if the elephant can move and we can't we don't have to
        # test that case b/c we'll get to the same state with our roles
        # flipped
        if after_me >= 0:
            # there's something we can move to and open

            # open it
            candidates.remove(candidate_me)

            # figure out what it will contribute once on
            contribution_me = rates[candidate_me] * after_me

            # now see where the elephant could go
            both = False
            for candidate_elephant in list(candidates):
                # how far away is it
                dist_elephant = dists[current_elephant][candidate_elephant]
                # what will t be once it gets there and opens it
                after_elephant = t_elephant - dist_elephant - 1

                if after_elephant >= 0:
                    # there's somewhere we both can move to and open

                    # open it
                    candidates.remove(candidate_elephant)

                    # figure out what it will contribute once on
                    contribution_elephant = (
                        rates[candidate_elephant] * after_elephant
                    )

                    # search from there adding anything we've accumilated so far
                    score = best_options(
                        candidate_me,
                        candidate_elephant,
                        after_me,
                        after_elephant,
                        pressure + contribution_me + contribution_elephant,
                        f'{prefix}  ',
                    )
                    options.append((score, candidate_me, candidate_elephant))

                    # close it
                    candidates.add(candidate_elephant)
                    both = True

            if not both:
                # if there wasn't an option for both just do mine
                score = best_options(
                    candidate_me,
                    current_elephant,
                    after_me,
                    0,
                    pressure + contribution_me,
                    f'{prefix}  ',
                )
                options.append((score, candidate_me, current_elephant))

            # close it
            candidates.add(candidate_me)

    # order options best to worst
    options.sort(reverse=True)

    if debug:
        print(
            f'results: current_me={current_me}, current_elephant={current_elephant}, t_me={t_me}, t_elephant={t_elephant}, pressure={pressure}'
        )
        for score, option_me, option_elephant in options:
            print(f'  {option_me} + {option_elephant} = {score}')

    try:
        # return the best option we found
        return options[0][0]
    except IndexError:
        # we didn't find any options, return what we were passed
        return pressure


best = best_options('AA', 'AA')
print(best)
