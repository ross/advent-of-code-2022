#!/usr/bin/env python3

from sys import stdin


def chunker(row):
    '''
    Stacks are 4 chars long. 4 spaces when empty and
    '[<char>]<space-or-newline>' when occupied. This helper splits the string
    it's passed into 4 character chunks. It's a generator that allows you to
    iterate over them
    '''
    for i in range(0, len(row), 4):
        yield row[i : i + 4]


stacks = None
for row in stdin:
    if '[' not in row:
        # we've hit the row with stack numbers, we're done reading stacks
        break
    if stacks == None:
        # first time through, figure out how many stacks we need, by dividing
        # the length of row by 4, see chunker for more info
        n = int(len(row) / 4)
        stacks = [list() for i in range(n)]
    # iterate over the chunks with their index
    for i, chunk in enumerate(chunker(row)):
        if '[' not in chunk:
            # its empty, skip it
            continue
        stacks[i].append(chunk[1])

# flip all the stacks to account for them being read from top to bottom and
# appended, thus backwards currently.
for stack in stacks:
    stack.reverse()

# skip the blank line between the stacks and operations
stdin.readline()

# we're now on to the operations section
for row in stdin:
    # get rid of the newline
    row.strip()
    # an operation is formatted as
    # move <N> from <S> to <D>
    # we'll split on whitepace and ignore the bits we don't need
    _, n, _, src, _, dst = row.split()
    # convert N to an integer from a string
    n = int(n)
    # same for src and dst, but we also need to subtract one to make them zero
    # indexed to match stacks
    src = int(src) - 1
    dst = int(dst) - 1
    # grab the src and dst stack we'll be working with
    src = stacks[src]
    dst = stacks[dst]
    # pop N items off of src appending them onto dst
    for i in range(n):
        dst.append(src.pop())

# create a string by joining the top of each stack
tops = ''.join((s[-1] for s in stacks))
print(tops)
