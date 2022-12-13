#!/usr/bin/env python3

from functools import cmp_to_key
from sys import stdin
from pprint import pprint


def compare(left, right, indent=''):
    left = list(left)
    right = list(right)
    print(f'{indent}- Compare {left} vs {right}')
    ret = None
    while ret is None and left and right:
        l1 = left.pop(0)
        r1 = right.pop(0)
        print(f'{indent}  - Compare {l1} vs {r1}')
        if isinstance(l1, int):
            # l1 is int
            if isinstance(r1, int):
                # both are ints, compare
                if l1 < r1:
                    print(
                        f'{indent}    - Left side is smaller, so inputs are in the right order'
                    )
                    ret = -1
                    break
                elif r1 < l1:
                    print(
                        f'{indent}    - Right side is smaller, so inputs are not in the right order'
                    )
                    ret = 1
                    break
            else:
                # r1 is a list, convert l1 to a list and traverse
                print(
                    f'{indent}    - Mixed types; convert left to [{l1}] and retry comparison'
                )
                ret = compare([l1], r1, indent=f'{indent}  ')
        else:
            # l1 is a list
            if isinstance(r1, int):
                # r1 is an int, convert it to a list
                print(
                    f'{indent}    - Mixed types; convert right to [{r1}] and retry comparison'
                )
                r1 = [r1]
            # then traverse the lists
            ret = compare(l1, r1, indent=f'{indent}  ')

    if ret is not None:
        # we already have an answer, return it
        return ret

    if not left and right:
        print(
            f'{indent}  - Left side ran out of items, so inputs are in the right order'
        )
        return -1
    elif left and not right:
        # right ran out first, inputs are in the wrong order
        print(
            f'{indent}  - Right side ran out of items, so inputs are not in the right order'
        )
        return 1

    # we've compared everything and gotten no answer, they're equal
    return None


divider_a = [[2]]
divider_b = [[6]]
packets = [divider_a, divider_b]
# split on blank lines to get pairs, omitting the final newline
for i, pair in enumerate(stdin.read()[:-1].split('\n\n')):
    packets.extend(eval(p) for p in pair.split('\n'))

pprint(packets)
packets.sort(key=cmp_to_key(compare))
pprint(packets)

prod = (packets.index(divider_a) + 1) * (packets.index(divider_b) + 1)
print(prod)
