#!/usr/bin/env python3

from sys import argv, stdin
from pprint import pprint

# 0,0 is lower left


class Knot:
    def __init__(self, id, verbose=False):
        self.id = id
        self.x = self.y = 0
        self.verbose = verbose


class Head(Knot):
    def __init__(self, *args, **kwargs):
        super().__init__('head', *args, **kwargs)
        self.d_x = self.d_y = 0

    def move(self, d_x, d_y):
        self.d_x = d_x
        self.d_y = d_y

    def tick(self):
        if self.d_x == 0 and self.d_y == 0:
            return False
        if self.verbose:
            pprint(
                {
                    'when': 'before',
                    'id': self.id,
                    'x': self.x,
                    'y': self.y,
                    'd_x': self.d_x,
                    'd_y': self.d_y,
                }
            )
        if self.d_x > 0:
            self.x += 1
            self.d_x -= 1
        elif self.d_x < 0:
            self.x -= 1
            self.d_x += 1
        if self.d_y > 0:
            self.y += 1
            self.d_y -= 1
        elif self.d_y < 0:
            self.y -= 1
            self.d_y += 1
        if self.verbose:
            pprint(
                {
                    'when': 'after',
                    'id': self.id,
                    'x': self.x,
                    'y': self.y,
                    'd_x': self.d_x,
                    'd_y': self.d_y,
                }
            )
        return True


class Follower(Knot):
    def __init__(self, id, leader, *args, **kwargs):
        super().__init__(id, *args, **kwargs)
        self.leader = leader
        self.cells_visited = set()
        # we need to visit our start point
        self.cells_visited.add((0, 0))

    def tick(self):
        d_x = self.leader.x - self.x
        d_y = self.leader.y - self.y
        if abs(d_x) == 0 and abs(d_y) == 0:
            return False
        if self.verbose:
            pprint(
                {
                    'when': 'before',
                    'id': self.id,
                    'x': self.x,
                    'y': self.y,
                    'd_x': d_x,
                    'd_y': d_y,
                }
            )
        # leader can only move up/down/left/right, but we can move diagonally when
        # we're off in both directions. To handle diagonals we first move a step
        # in the direction where we're 2 away, and then add any mis-alignment in
        # the other direction, if any
        if d_x > 1:
            self.x += 1
            if d_y > 0:
                self.y += 1
            elif d_y < 0:
                self.y -= 1
        elif d_x < -1:
            self.x -= 1
            if d_y > 0:
                self.y += 1
            elif d_y < 0:
                self.y -= 1
        elif d_y > 1:
            self.y += 1
            if d_x > 0:
                self.x += 1
            elif d_x < 0:
                self.x -= 1
        elif d_y < -1:
            self.y -= 1
            if d_x > 0:
                self.x += 1
            elif d_x < 0:
                self.x -= 1

        # flag that we visited our current cell
        self.cells_visited.add((self.y, self.x))

        if self.verbose:
            pprint(
                {
                    'when': 'after',
                    'id': self.id,
                    'x': self.x,
                    'y': self.y,
                    'leader.x': self.leader.x,
                    'leader.y': self.leader.y,
                }
            )
        return True

    @property
    def num_cells_visited(self):
        # we have inserted a 1 in each cell we visited, so if we sum the rows
        # and then sum the sums we'll have a count of the number of cells
        # visited
        return len(self.cells_visited)


verbose = 'verbose' in argv or 'all' in argv
verbose_main = verbose or 'main' in argv
verbose_head = verbose or 'head' in argv
verbose_followers = verbose or 'followers' in argv

head = Head(verbose=verbose_head)
# create the follower chain
prev = head
followers = []
for i in range(1, 10):
    verbose_follower = verbose_followers or f'follower_{i}' in argv
    follower = Follower(i, prev, verbose=verbose_follower)
    followers.append(follower)
    prev = follower

for move in stdin:
    direction, steps = move.strip().split(' ')
    steps = int(steps)
    d_x = d_y = 0
    if direction == 'R':
        d_x = steps
    elif direction == 'L':
        d_x = -steps
    elif direction == 'U':
        d_y = steps
    else:  # direction == 'D':
        d_y = -steps

    if verbose_main:
        pprint({'direction': direction, 'steps': steps, 'd_x': d_x, 'd_y': d_y})

    # provide the head its target
    head.move(d_x, d_y)

    # and tick things until the head is done moving, followers will get the same
    # number of ticks
    while head.tick():
        for follower in followers:
            follower.tick()

    if verbose_main:
        pprint(
            {
                'head': {'x': head.x, 'y': head.y},
                'followers': [
                    {'id': f.id, 'x': f.x, 'y': f.y} for f in followers
                ],
            }
        )

print(followers[-1].num_cells_visited)
