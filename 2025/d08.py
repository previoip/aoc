from itertools import combinations
from math import sqrt

def parser(inp):
  for line in inp.splitlines():
    yield tuple(map(int, line.split(',')))

def l1normsq(va, vb):
  return (va[0]-vb[0])**2 + \
  (va[1]-vb[1])**2 + \
  (va[2]-vb[2])**2

def amin(arr):
  t = 1e10
  j = -1
  for i, v in enumerate(arr):
    if v < 0: continue
    if v < t:
      j = i
      t = v
  return j

def part1(inp):
  junctions = list(parser(inp))
  njunction = len(junctions)
  dists = [[-1 for _ in range(njunction)] for _ in range(njunction)]

  for a, b in combinations(range(njunction), 2):
    if a==b: continue
    norm = sqrt(l1normsq(junctions[a], junctions[b]))
    dists[b][a] = norm
    dists[a][b] = norm

  def closest_takewhile():
    while True:
      rowsmi = [amin(row) for row in dists]
      if all([i==-1 for i in rowsmi]):
        yield None
      rowsmv = [dists[i][j] for i, j in enumerate(rowsmi)]
      col = amin(rowsmv)
      row = rowsmi[col]
      dists[row][col] = -1
      dists[col][row] = -1
      yield col, row

  circs = [{i} for i in range(njunction)]
  for _ in range(10):
    tup = next(closest_takewhile())
    if tup is None: break
    a, b = tup
    circs[a].update(circs[b])
    for da in circs[a]:
      circs[da].update(circs[b])
    circs[b].update(circs[a])
    for db in circs[b]:
      circs[db].update(circs[a])
    print(junctions[a], junctions[b], circs[b], circs[a])

  circu = set()
  for circ in circs:
    circu.add(frozenset(circ))

  circl = [len(i) for i in circu]
  circl = sorted(circl)

  muls = circl.pop()
  for _ in range(2):
    muls *= circl.pop()
  return muls


def part2(inp):
  junctions = list(parser(inp))
  njunction = len(junctions)
  dists = [[-1 for _ in range(njunction)] for _ in range(njunction)]

  for a, b in combinations(range(njunction), 2):
    if a==b: continue
    norm = sqrt(l1normsq(junctions[a], junctions[b]))
    dists[b][a] = norm
    dists[a][b] = norm

  def closest_takewhile():
    while True:
      rowsmi = [amin(row) for row in dists]
      if all([i==-1 for i in rowsmi]):
        yield None
      rowsmv = [dists[i][j] for i, j in enumerate(rowsmi)]
      col = amin(rowsmv)
      row = rowsmi[col]
      dists[row][col] = -1
      dists[col][row] = -1
      yield col, row

  circs = [{i} for i in range(njunction)]
  a = 0
  b = 0
  c = 0
  while True:
    c += 1
    tup = next(closest_takewhile())
    if tup is None: break
    a, b = tup
    circs[a].update(circs[b])
    for da in circs[a]:
      circs[da].update(circs[b])
    circs[b].update(circs[a])
    for db in circs[b]:
      circs[db].update(circs[a])
    if len(circs[a]) == njunction: break
    print(f'{c:05d}', junctions[a], junctions[b], len(circs[a]))
  print(junctions[a], junctions[b], circs[b], circs[a])
  return junctions[a][0] * junctions[b][0]
