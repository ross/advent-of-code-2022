#!/usr/bin/env python3

from sys import argv, stdin
from pprint import pprint


class Monkey:
    def __init__(self, config, debug=False):
        self.debug = debug

        config = config.split('\n')
        if self.debug:
            pprint(config)
        # id
        self.id = int(config[0][:-1].split(' ', 1)[1])
        # starting items
        self.items = [int(v) for v in config[1].split(': ')[1].split(', ')]
        # operation
        line = config[2]
        if 'old * old' in line:
            self.op = lambda old: old * old
        elif '+' in line:
            value = int(line.rsplit(' ', 1)[1])
            self.op = lambda old: old + value
        elif '*' in line:
            value = int(line.rsplit(' ', 1)[1])
            self.op = lambda old: old * value
        else:
            raise Exception('unhandled operation')
        # test
        self.divisor = int(config[3].rsplit(' ', 1)[1])
        # monkey if true
        self.if_true = int(config[4].rsplit(' ', 1)[1])
        # monkey if false
        self.if_false = int(config[5].rsplit(' ', 1)[1])

        if self.debug:
            pprint(
                {
                    'id': self.id,
                    'items': self.items,
                    'op': self.op,
                    'divisor': self.divisor,
                    'if_true': self.if_true,
                    'if_false': self.if_false,
                }
            )

        self.inspected = 0

    def turn(self, prod):
        for item in self.items:
            self.inspected += 1
            if self.debug:
                print(f'item={item}')
            # perform our operation
            item = self.op(item)
            if self.debug:
                print(f'  post op={item}')
            # so the monkeys don't care what the item's worry level actually is,
            # they just care about whether it's divisible by their divisor. in
            # order to keep the worry levels in check we'll mod them by the
            # product of all the monkey's divisors. this will preserve the
            # results of our checking with % while keeping the numbers small
            # enough to avoid the slow and expensive python large number support
            # (that might work, but not for a very very long time.)
            item %= prod
            if self.debug:
                print(f'  post % {prod}={item}')
            # decide where to throw it based on whether or not it divides
            # evenly, no remainer
            target = self.if_false if item % self.divisor else self.if_true
            if self.debug:
                print(f'  item % {self.divisor}={item % self.divisor}')
                print(f'  target={target}')
            yield item, target

        # we've thrown all of our items
        self.items = []

    def catch(self, item):
        if self.debug:
            print(f'{self.id} caught {item}')
        self.items.append(item)


debug = 'debug' in argv
debug_monkey = debug or 'debug_monkey' in argv
debug_turns = debug or 'debug_turns' in argv

monkeys = {}
order = []
prod = 1
for config in stdin.read().split('\n\n'):
    monkey = Monkey(config, debug=debug_monkey)
    monkeys[monkey.id] = monkey
    order.append(monkey)
    prod *= monkey.divisor

for turn in range(10000):
    for monkey in order:
        for item, target in monkey.turn(prod):
            recipient = monkeys[target]
            recipient.catch(item)

    if debug_turns:
        print(f'Turn {turn+1}')
        for monkey in order:
            items = ' '.join(str(v) for v in monkey.items)
            print(f'Monkey {monkey.id}: {items}')

    turn += 1
    if turn in (1, 20) or turn % 1000 == 0:
        print(f'== After round {turn} ==')
        for monkey in order:
            print(
                f'Monkey {monkey.id} inspected items {monkey.inspected} times.'
            )

inspected = sorted((m.inspected for m in order), reverse=True)
monkey_business = inspected[0] * inspected[1]
print(f'Monkey business: {inspected[0]} * {inspected[1]} = {monkey_business}')
