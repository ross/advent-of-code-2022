#!/usr/bin/env python3

from collections import defaultdict
from pprint import pprint
from sys import stdin


def parents(path):
    for i in range(len(path)):
        yield path[:-i]


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
        command['output'].append(row)

pprint({'commands': commands})

sizes = defaultdict(lambda: 0)
path = tuple()
for command in commands:
    pprint({'command': command, 'path': path})
    exe = command['exe']
    if exe == 'cd':
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

pprint(sizes)

total_disk = 70000000
# available disk space is ^ minus /'s size
available_disk = total_disk - sizes[tuple()]
update_requires = 30000000
need_to_free = update_requires - available_disk

pprint(
    {
        'total_disk': total_disk,
        'available_disk': available_disk,
        'update_requires': update_requires,
        'need_to_free': need_to_free,
    }
)

# find directories that are large enough to give us the required space when
# deleted, we don't care about paths
candidates = [s for s in sizes.values() if s > need_to_free]

pprint({'candidates': candidates})

# sort them smallest to largest
candidates.sort()

pprint({'sorted': candidates})

# the first one is our best option, we're after its size
print(candidates[0])
