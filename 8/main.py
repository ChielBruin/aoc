import sys, re

def collect(layer, f):
    for row in layer:
        for e in row:
            if f(e):
                yield e

def push_pixel(bitmap, layer_idx, row_idx, column_idx, value):
    if len(bitmap) == layer_idx:
        bitmap.append([])
    if len(bitmap[layer_idx]) == row_idx:
        bitmap[layer_idx].append([])
    if not len(bitmap[layer_idx][row_idx]) == column_idx:
        raise Exception('invalid bitmap state')
    bitmap[layer_idx][row_idx].append(value)

lines = sys.stdin.read().split('\n')
width, height = tuple(map(int, re.match(r'([\d]+)x([\d]+)', lines[1]).group(1,2)))

input = [int(x) for x in lines[2]]

layers = []
for idx, c in enumerate(input):
    layer_idx = idx // (width * height)
    row_idx = (idx // width) % height
    column_idx = idx % width
    push_pixel(layers, layer_idx, row_idx, column_idx, c)

zeros = map(lambda x: len(list(collect(x, lambda v: v == 0))), layers)
min = (sys.maxsize, -1)
for i, val in enumerate(zeros):
    if val < min[0]:
        min = (val, i)


ones = len(list(collect(layers[min[1]], lambda v: v == 1)))
twos = len(list(collect(layers[min[1]], lambda v: v == 2)))

print('Ones times twos:')
print(ones * twos)

# Part 2:

def underlay_layers(top, bottom):
  for x in range(len(top)):
    for y in range(len(top[x])):
        if top[x][y] == 2:
            top[x][y] = bottom[x][y]

output = layers[0].copy()
for layer in layers[1:]:
    underlay_layers(output, layer)

print(output)
