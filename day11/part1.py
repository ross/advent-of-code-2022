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

    def turn(self):
        for item in self.items:
            self.inspected += 1
            if self.debug:
                print(f'item={item}')
            # perform our operation
            item = self.op(item)
            if self.debug:
                print(f'  post op={item}')
            # divide by 3 and round down due to relief
            item = int(item / 3)
            if self.debug:
                print(f'  divided and rounded={item}')
            # decide where to throw it based on whether or not it divides
            # evenly, no remainer
            target = self.if_false if item % self.divisor else self.if_true
            if self.debug:
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
for config in stdin.read().split('\n\n'):
    monkey = Monkey(config, debug=debug_monkey)
    monkeys[monkey.id] = monkey
    order.append(monkey)

for turn in range(20):
    for monkey in order:
        for item, target in monkey.turn():
            recipient = monkeys[target]
            recipient.catch(item)

    if debug_turns:
        print(f'Turn {turn+1}')
        for monkey in order:
            items = ' '.join(str(v) for v in monkey.items)
            print(f'Monkey {monkey.id}: {items}')


for monkey in order:
    print(f'Monkey {monkey.id} inspected items {monkey.inspected} times.')

inspected = sorted((m.inspected for m in order), reverse=True)
monkey_business = inspected[0] * inspected[1]
print(f'Monkey business: {inspected[0]} * {inspected[1]} = {monkey_business}')
