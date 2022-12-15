#!/usr/bin/env python

from sys import argv, stdin
import re


def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Sensor:
    def __init__(self, sensor_x, sensor_y, beacon_x, beacon_y):
        self.x = int(sensor_x)
        self.y = int(sensor_y)
        self.beacon_x = int(beacon_x)
        self.beacon_y = int(beacon_y)
        self.distance = manhattan_distance(
            self.x, self.y, self.beacon_x, self.beacon_y
        )

    def __repr__(self):
        return f'<{self.x:6d}, {self.y:6d}> -> {self.beacon_x:6d}, {self.beacon_y:6d}'


class Cave:
    def __init__(self, sensors):
        self.sensors = sensors

    def available(self, y, max_x):
        spans = []
        for sensor in self.sensors:
            # how far is the sensor from the desired row
            dy = abs(sensor.y - y)
            if dy > sensor.distance:
                # we're not interested in this one
                continue
            # how big a swath will it make in this row
            dx = sensor.distance - dy
            # use that to figure out its start and end point
            start = sensor.x - dx
            end = sensor.x + dx
            # don't care about things that end before our range or start after
            # it
            if end >= 0 and start <= max_x:
                spans.append((start, end))

        # sort the spans (by their start points)
        spans.sort()

        # grab the end of the first span
        end = spans[0][1]
        # for the rest of the spans
        for span in spans[1:]:
            # grab its start
            start = span[0]
            # if there's a gap between this one's start and our current end
            if start - end > 0:
                # we've found what we're looking for
                return start - 1, y
            # otherwise, if the new span ends after our current end
            if span[1] > end:
                # update our end
                end = span[1]

        # no gaps found
        return None, None


parser = re.compile(
    r'x=(?P<sensor_x>-?\d+), y=(?P<sensor_y>-?\d+):.* x=(?P<beacon_x>-?\d+), y=(?P<beacon_y>-?\d+)'
)
sensors = []
for line in stdin:
    match = parser.search(line)
    sensor = Sensor(**match.groupdict())
    sensors.append(sensor)

cave = Cave(sensors)
maximum = int(argv[1])
# from 0 to maximum
for y in range(maximum + 1):
    # look for a gap
    x, y = cave.available(y, maximum)
    if x is not None:
        # we found one
        break

# calculate the frequency
print(f'x={x}, y={y}, freq={x*4000000+y}')
