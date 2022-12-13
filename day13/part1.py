#!/usr/bin/env python3

from sys import stdin
from pprint import pprint


def correct(left, right, indent=''):
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
                    ret = True
                    break
                elif r1 < l1:
                    print(
                        f'{indent}    - Right side is smaller, so inputs are not in the right order'
                    )
                    ret = False
                    break
            else:
                # r1 is a list, convert l1 to a list and traverse
                print(
                    f'{indent}    - Mixed types; convert left to [{l1}] and retry comparison'
                )
                ret = correct([l1], r1, indent=f'{indent}  ')
        else:
            # l1 is a list
            if isinstance(r1, int):
                # r1 is an int, convert it to a list
                print(
                    f'{indent}    - Mixed types; convert right to [{r1}] and retry comparison'
                )
                r1 = [r1]
            # then traverse the lists
            ret = correct(l1, r1, indent=f'{indent}  ')

    if ret is not None:
        # we already have an answer, return it
        return ret

    if not left and right:
        print(
            f'{indent}  - Left side ran out of items, so inputs are in the right order'
        )
        return True
    elif left and not right:
        # right ran out first, inputs are in the wrong order
        print(
            f'{indent}  - Right side ran out of items, so inputs are not in the right order'
        )
        return False

    # we've compared everything and gotten no answer
    return None


total = 0
# split on blank lines to get pairs, omitting the final newline
for i, pair in enumerate(stdin.read()[:-1].split('\n\n')):
    # we're asked to do one-indexed
    i += 1
    print(f'== Pair {i} ==')
    left, right = pair.split('\n')
    # the lists happen to be valid python so take advantage of it
    left = eval(left)
    right = eval(right)
    if False:
        pprint({'i': i, 'pair': pair, 'left': left, 'right': right})
    if correct(left, right):
        total += i
    print()

print(total)
