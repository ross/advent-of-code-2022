#!/usr/bin/env python3

from collections import defaultdict
from sys import stdin


def parents(path):
    for i in range(len(path)):
        yield path[:-i]


# parse our commands and their output
commands = []
for row in stdin:
    row = row.strip()
    if row[0] == '$':
        # it's a new command
        cmdline = row[2:].split(' ')
        exe = cmdline[0]
        args = cmdline[1:]
        command = {'exe': exe, 'args': args, 'output': []}
        commands.append(command)
    else:
        # it's output from the most recent command, append it
        command['output'].append(row)

# now process the commands to calculate directory sizes
sizes = defaultdict(lambda: 0)
#  our current path
path = tuple()
for command in commands:
    exe = command['exe']
    if exe == 'cd':
        # the arg is the directory change to be made
        arg = command['args'][0]
        if arg == '/':
            # change to root
            path = tuple()
        elif arg == '..':
            # go up one level to our parent
            path = path[:-1]
        else:  # a child
            # go down one level to a child
            path = path + (arg,)
    elif exe == 'ls':
        # some of the output lines will contain file sizes
        for line in command['output']:
            try:
                # split the output line, if we can convert the first piece to
                # an int then it's a filesize and needs to be counted
                size = int(line.split(' ', 1)[0])
            except ValueError:
                # otherwise it's a child directory and can be ignored, move on
                # to the next output line
                continue
            # we have a file size, it needs to be added to our current path
            sizes[path] += size
            # and then to each parent of the current directory
            for parent in parents(path):
                sizes[parent] += size

# iterate over all of the directory sizes (we don't care about names) summing
# all the directories with less then 100000
total = 0
for size in sizes.values():
    if size < 100000:
        total += size

print(total)
