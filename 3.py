import re, sys

def acc_map(iterable, acc, func):
    for elem in iterable:
        for acc in func(elem, acc):
            yield acc

def step(elem, loc):
    (x, y, s) = loc
    dir, steps = re.match(r'([RLUD])([\d]+)', elem).group(1,2)
    steps = int(steps)
    for i in range(steps):
        if dir == 'R':
            x += 1
        elif dir == 'L':
            x -= 1
        elif dir == 'U':
            y += 1
        elif dir == 'D':
            y -= 1
        else:
            raise Exception('Unknown direction %s' % dir)
        yield (x, y, s+1 + i)

def dist(x, y):
    return (x if x > 0 else -x) + (y if y > 0 else -y)

def collide(lines):
    buckets = {}
    for idx, line in enumerate(lines):
        for coord in line:
            x, y, s = coord
            d = dist(x, y)
            if d not in buckets:
                buckets[d] = {(x,y): [(idx, s)]}
            else:
                if (x,y) in buckets[d]:
                    for (o_idx, o_s) in buckets[d][(x,y)]:
                        if not idx is o_idx:
                            yield (x, y, (idx, s), (o_idx, o_s))

                buckets[d][(x,y)] = [(idx,s)]

def filter_part1(collisions):
    for (x, y, l1, l2) in collisions:
        yield dist(x, y)


def filter_part2(collisions):
    for (x, y, (l1, s1), (l2, s2)) in collisions:
        yield s1 + s2

in_str = sys.stdin.read()
lines = [acc_map(line.split(','), (0,0,0), step) for line in in_str.split('\n') if line]

print(min(filter_part1(collide(lines))))
# print(min(filter_part2(collide(lines))))
