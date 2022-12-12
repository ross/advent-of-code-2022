#!/usr/bin/env python3

from sys import argv, setrecursionlimit, stdin
from pprint import pprint


class Map:
    MAX_STEPS = UNVISITED = 99999

    def __init__(self, grid, debug):
        self.grid = grid
        self.debug = debug

        # blank path
        scores = [[self.MAX_STEPS] * len(grid[0]) for _ in range(len(grid))]
        self.scores = scores

    def print_grid(self):
        print('\n'.join((''.join(r) for r in self.grid)))

    def print_scores(self):
        print('\n'.join((' '.join(f'{c:05d}' for c in r) for r in self.scores)))

    @classmethod
    def can_step(cls, current, candidate):
        # we're going in reverse so we'll never be on start, only stepping to it
        # so check candidate for it
        if candidate == 'S':
            # start is equivalent to 'a'
            candidate = 'a'
        # and we'll only be on the end, never stepping to it. so check current
        # for it
        if current == 'E':
            # end is equivalent to 'z'
            current = 'z'
        return candidate >= current or (ord(current) - ord(candidate) < 2)

    def search(self):
        # find our end
        for y, row in enumerate(self.grid):
            try:
                x = row.index('E')
                break
            except ValueError:
                # not in this row
                pass

        # from there search out marking each cell with its shortest distance
        # from the end
        self._search(y, x, 0)

        if self.debug:
            self.print_scores()

        # find our end
        for y, row in enumerate(self.grid):
            try:
                x = row.index('S')
                break
            except ValueError:
                # not in this row
                pass

        # its score will be the shortest path
        return self.scores[y][x]

    def _search(self, y, x, distance):
        if self.debug:
            print(f'_search: y={y}, x={x}, distance={distance}')

        # we've stepped onto the cell, so mark its distance
        self.scores[y][x] = distance

        # figure out how high we are
        elevation = self.grid[y][x]
        if self.debug:
            pprint(
                {'y': y, 'x': x, 'elevation': elevation, 'distance': distance}
            )

        next_step = distance + 1

        if y > 0 and next_step < self.scores[y - 1][x]:
            # there's something above us, and its score is worse than if we step
            # there now
            up = grid[y - 1][x]
            if self.can_step(elevation, up):
                # we can step there
                self._search(y - 1, x, next_step)

        if y + 1 < len(grid) and next_step < self.scores[y + 1][x]:
            # there's something below us, and its score is worse than if we step
            # there now
            down = grid[y + 1][x]
            if self.can_step(elevation, down):
                # we can step there
                self._search(y + 1, x, next_step)

        if x > 0 and next_step < self.scores[y][x - 1]:
            # there's something left of us, and its score is worse than if we
            # step there now
            left = grid[y][x - 1]
            if self.can_step(elevation, left):
                self._search(y, x - 1, next_step)

        if x + 1 < len(grid[y]) and next_step < self.scores[y][x + 1]:
            # there's something right of us, and its score is worse than if we
            # step there now
            right = grid[y][x + 1]
            if self.can_step(elevation, right):
                self._search(y, x + 1, next_step)


grid = []
for y, row in enumerate(stdin):
    row = row.strip()
    # convert to array of chars so that we can assign
    grid.append([c for c in row])


debug = 'debug' in argv

# make sure we can recurse as deeply as the number of steps Map supports
setrecursionlimit(Map.MAX_STEPS)

m = Map(grid, debug=debug)
m.print_grid()
n = m.search()
m.print_scores()
print(f'Shortest path is {n} steps')
