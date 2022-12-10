#!/usr/bin/env python3

from sys import argv, stdin
from pprint import pprint


class Cpu:
    def __init__(self, debug=False):
        self.X = 1
        self.cycle = 0
        self.debug = debug
        self.summed_signal_strengths = 0

    def _tick(self):
        self.cycle += 1
        # 20th and every 40th after that
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            signal_strength = self.cycle * self.X
            print(
                f'cycle={self.cycle}, X={self.X}, cycle * X={signal_strength}'
            )
            self.summed_signal_strengths += signal_strength

    def exec(self, op, args):
        op = getattr(self, op)
        op(*args)
        if self.debug:
            pprint({'op': op, 'args': args, 'cycle': self.cycle, 'X': self.X})

    def addx(self, value):
        self._tick()
        self._tick()
        self.X += int(value)

    def noop(self):
        self._tick()


debug = 'debug' in argv
debug_parse = debug or 'debug_parse' in argv
debug_cpu = debug or 'debug_cpu' in argv

cpu = Cpu(debug=debug_cpu)
for line in stdin:
    pieces = line.strip().split(' ')
    op = pieces[0]
    args = pieces[1:]
    if debug_parse:
        pprint({'pieces': pieces, 'op': op, 'args': args})

    cpu.exec(op, args)

print(cpu.summed_signal_strengths)
