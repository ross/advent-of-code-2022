#!/usr/bin/env python

from pprint import pprint
from sys import argv, stdin


class Cave:
    def __init__(self, paths, debug=False):
        self.debug = debug

        # find our mins and maxes, we'll just find the max y as our y size
        # directly since we'll only be translating x
        x_min = 999999
        x_max = y_size = -999999
        for path in paths:
            for step in path:
                x, y = step
                if x < x_min:
                    x_min = x
                elif x_max < x:
                    x_max = x
                elif y_size < y:
                    y_size = y

        # add two more rows so we have room for the floor
        y_size += 2
        # expand X's by +/- y size so that we're sure that things can pile up to
        # reach the drop point if needed
        x_min -= y_size
        x_max += y_size

        # find our x size
        x_size = x_max - x_min

        floor = ((0, y_size), (x_size, y_size))

        if self.debug:
            pprint(
                {
                    'paths': paths,
                    'floor': floor,
                    'ranges': {'x': (x_min, x_max, x_size), 'y': (y_size)},
                }
            )

        # create our blank grid, y rows, x cols in each row to match problem
        # examples 0,0 is top-left and y goes down the vertical axis, x across
        # the horizontal
        self.grid = [['.'] * (x_size + 1) for _ in range(y_size + 1)]

        for path in paths:
            self.draw_path(path, x_min)

        # draw the floor
        self.draw_path(floor)

        self.drop_point = (500 - x_min, 0)
        self.grid[0][self.drop_point[0]] = '+'

        self.draw_grid()

    def draw_path(self, path, x_min=0):
        if self.debug:
            pprint({'path': path})
        start = path[0]
        for end in path[1:]:
            self.draw_line(start, end, x_min)
            start = end

    def draw_line(self, start, end, x_min=0):
        if self.debug:
            pprint({'start': start, 'end': end})

        x_start = start[0]
        y_start = start[1]
        x_end = end[0]
        y_end = end[1]

        if self.debug:
            pprint(
                {
                    'x_start': x_start,
                    'x_end': x_end,
                    'y_start': y_start,
                    'y_end': y_end,
                }
            )

        if x_start > x_end:
            x_start, x_end = x_end, x_start
        if y_start > y_end:
            y_start, y_end = y_end, y_start

        if self.debug:
            pprint(
                {
                    'x_start': x_start,
                    'x_end': x_end,
                    'y_start': y_start,
                    'y_end': y_end,
                }
            )

        # translate x points to our origin
        x_start = x_start - x_min
        x_end = x_end - x_min

        if x_start == x_end:
            # line is vertical
            for y in range(y_start, y_end + 1):
                self.grid[y][x_start] = '#'
        else:  # line is horizontal
            for x in range(x_start, x_end + 1):
                self.grid[y_start][x] = '#'

    def draw_grid(self):
        for line in self.grid:
            print(''.join(line))

    def drop(self):
        # start at our drop point
        x, y = self.drop_point
        n = len(self.grid)
        while True:
            if y + 1 == n:
                # we fell off to infinity/didn't land
                return False
            if self.grid[y + 1][x] == '.':
                # fall straight down
                y += 1
            elif self.grid[y + 1][x - 1] == '.':
                # fall down and to the left
                y += 1
                x -= 1
            elif self.grid[y + 1][x + 1] == '.':
                # fall down and to the right
                y += 1
                x += 1
            else:
                # can't fall anymore
                break

        self.grid[y][x] = 'o'

        # when y == drop point we've landed on the origin and we're done
        return y != self.drop_point[1]


# parse paths
paths = []
for row in stdin:
    row = row.strip()
    path = []
    for point in row.split(' -> '):
        path.append(tuple(int(v) for v in point.split(',')))
    paths.append(path)


debug = 'debug' in argv

# create cave
cave = Cave(paths, debug=debug)
i = 1
while cave.drop():
    i += 1

print(f'Grain {i}')
cave.draw_grid()
print(i)
