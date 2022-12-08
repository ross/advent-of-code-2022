#!/usr/bin/env python3

from sys import stdin


# load our trees into a 2d array
trees = []
for row in stdin:
    row = row.strip()
    row = [int(v) for v in row]
    trees.append(row)

# create the inverse of the trees array, this will make it easier to get our up
# and down slices below
# see https://stackoverflow.com/a/20279160 for a thorough explination
inv_trees = list(list(v) for v in zip(*trees))


def look_out(run, height):
    '''
    Accepts a run of trees and returns how many trees can be seen from left to
    right in it.
    '''
    if not run:
        # we were on an edge, no trees can be seen
        return 0
    for i, tree in enumerate(run):
        # run until we see a tree as tall as we are or taller
        if tree >= height:
            break
    # then add one since we're zero indexed
    return i + 1


best = 0
# for each tree
for y in range(len(trees)):
    # we'll use the trees as read for left and right
    row = trees[y]
    for x in range(len(row)):
        # we'll use the inverse trees (columns are rows) for up and down,
        # we'll need to index with the column/x var of our current tree to get
        # the slice we're after
        inv_row = inv_trees[x]

        # find the current tree's height
        height = row[x]

        # to the left, everything before our column
        left = row[:x]
        # reverse so that things are going away from the tree
        left.reverse()
        left = look_out(left, height)

        # right, everythig after our column
        right = row[x + 1 :]
        right = look_out(right, height)

        # up, everything before our row
        up = inv_row[:y]
        # reverse so that things are going away from the tree
        up.reverse()
        up = look_out(up, height)

        # down, everything after our row
        down = inv_row[y + 1 :]
        down = look_out(down, height)

        # calculate our scenic score
        score = left * right * up * down

        # if it's the best we've seen so far
        if score > best:
            # store it
            best = score

print(best)
