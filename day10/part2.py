#!/usr/bin/env python3

from sys import argv, stdin
from pprint import pprint


class Screen:
    def __init__(self, debug):
        self.debug = debug

        # initially everything is dark
        self.pixels = [['.'] * 40 for _ in range(6)]
        self.y = self.x = 0
        if self.debug:
            self.display()

    def display(self):
        # print out each row, joining columns without any space
        for row in self.pixels:
            print(''.join(row))

    def tick(self, X):
        if abs(X - self.x) < 2:
            # sprite (3 pixels wide) lines up with the pixel we're currently
            # drawing so mark it on
            self.pixels[self.y][self.x] = 'X'
        else:
            # this pixel is dark so mark it off
            self.pixels[self.y][self.x] = '.'
        # advance the col
        self.x += 1
        if self.x > 39:
            # if we've gone past the end wrap x and advance y
            self.x = 0
            self.y += 1
            if self.y > 5:
                # if we've gone past the last row, wrap y as well
                self.y = 0

        if self.debug:
            pprint({'x': self.x, 'y': self.y, 'X': X})
            self.display()


class Cpu:
    def __init__(self, screen, debug=False):
        self.screen = screen
        self.debug = debug

        self.X = 1

    def _tick(self):
        self.screen.tick(self.X)

    def exec(self, op, args):
        op = getattr(self, op)
        op(*args)
        if self.debug:
            pprint({'X': self.X})

    def addx(self, value):
        self._tick()
        self._tick()
        self.X += int(value)

    def noop(self):
        self._tick()


debug = 'debug' in argv
debug_parse = debug or 'debug_parse' in argv
debug_screen = debug or 'debug_screen' in argv
debug_cpu = debug or 'debug_cpu' in argv

screen = Screen(debug=debug_screen)
cpu = Cpu(screen=screen, debug=debug_cpu)
for line in stdin:
    pieces = line.strip().split(' ')
    op = pieces[0]
    args = pieces[1:]
    if debug_parse:
        pprint({'pieces': pieces, 'op': op, 'args': args})

    cpu.exec(op, args)

screen.display()
