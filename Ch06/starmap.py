from itertools import starmap
xs = [7, 3, 1, 19, 11]
ys = [8, 1, -3, 14, 22]

loop_maxes = [max(ys[i], x) for i, x in enumerate(xs)]
map_maxes = list(starmap(max, zip(xs, ys)))

print(loop_maxes)
# [8, 3, 1, 19, 22]
print(map_maxes)
# [8, 3, 1, 19, 22]
