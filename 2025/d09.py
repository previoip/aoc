from itertools import combinations
from functools import cache

def parser(inp):
  for line in inp.splitlines():
    yield tuple(map(int, line.split(',')))


def amax(arr):
  t = 0
  j = -1
  for i, v in enumerate(arr):
    if v < 0: continue
    if v > t:
      j = i
      t = v
  return j  

def calcArea(p1, p2):
  ax, ay = p1
  bx, by = p2
  dx = abs(ax-bx)+1
  dy = abs(ay-by)+1
  return dx*dy


def part1(inp):
  coos = list(parser(inp))
  nitems = len(coos)
  areas = [[-1 for _ in range(nitems)] for _ in range(nitems)]
  for a, b in combinations(range(nitems), 2):
    area = calcArea(coos[a], coos[b])
    areas[a][b] = area
    areas[b][a] = area
  rowmaxv = [None for _ in range(nitems)]
  for i in range(nitems):
    rowmaxv[i] = areas[i][amax(areas[i])]
  return max(rowmaxv)


def xyhilo(xl, yl, xh, yh):
  t = 0
  if xl > xh:
    t = xh
    xh = xl
    xl = t
  if yl > yh:
    t = yh
    yh = yl
    yl = t
  return xl, yl, xh, yh


def issubset(p, p1, p2):
  xl, yl = p1
  xh, yh = p2
  xl, yl, xh, yh = xyhilo(xl, yl, xh, yh)
  xx = (p[0] > xl) and (p[0] < xh)
  yy = (p[1] > yl) and (p[1] < yh)
  return xx and yy


_isinside_cache = dict()
def isinside(p, coos):
  if p in _isinside_cache:
    return _isinside_cache[p]
  inside = False
  lx = coos[0][0]
  ly = coos[0][1]
  hx = coos[0][0]
  hy = coos[0][1]
  for coo in coos:
    lx = min(lx, coo[0])
    ly = min(ly, coo[1])
    hx = max(hx, coo[0])
    hy = max(hy, coo[1])
  if p[0] < lx or p[0] > hx or p[1] < ly or p[1] > hy:
    return False
  #  https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
  nvert = len(coos)
  testx = p[0]
  testy = p[1]
  for i in range(nvert):
    e0 = coos[i]
    e1 = coos[(i+1) % nvert]
    vertxi = e0[0]
    vertxj = e1[0]
    vertyi = e0[1]
    vertyj = e1[1]
    if ((vertyi > testy) != (vertyj > testy)) and \
    (testx < (vertxj-vertxi) * (testy-vertyi) / (vertyj-vertyi) + vertxi):
      inside = not inside
  _isinside_cache[p] = inside
  return inside

_isinsideshifted_cache = dict()
def isinsideshifted(p, coos):
  if p in _isinsideshifted_cache:
    return _isinsideshifted_cache[p]
  inside = isinside(p, coos)
  inside |= isinside((p[0]-1, p[1]-1), coos)
  inside |= isinside((p[0]-1, p[1]  ), coos)
  inside |= isinside((p[0]  , p[1]-1), coos)
  _isinsideshifted_cache[p] = inside
  return inside

def ckvalid(p1, p2, coos):
  for pt in coos:
    if pt == p1 or pt == p2: continue
    if issubset(pt, p1, p2):
      return False
    xl, yl, xh, yh = xyhilo(*p1, *p2)
    for p in [
      (xl, yl),
      (xl, yh),
      (xh, yl),
      (xh, yh),
    ]:
      if not isinsideshifted(p, coos):
        return False
  return True

def drawtile(coos, pp=None):
  xs = [i[0] for i in coos]
  ys = [i[1] for i in coos]
  buf = [['.' for _ in range(max(xs)+4)]for _ in range(max(ys)+4)]
  for x, y in coos:
    buf[y][x] = '#'
  for x in range(max(xs)+4):
    for y in range(max(ys)+4):
      if isinsideshifted((x, y), coos):
        buf[y][x] = 'x'
  if not pp is None:
    xl, yl = pp[0]
    xh, yh = pp[1]
    xl, yl, xh, yh = xyhilo(xl, yl, xh, yh)
    for x in range(xl, xh+1):
      for y in range(yl, yh+1):
        buf[y][x] = 'O'
  for row in buf:
    print(''.join(row))


def part2(inp):
  coos = list(parser(inp))
  nitems = len(coos)
  maxarea = 0  
  for a, b in combinations(range(nitems), 2):
    if not ckvalid(coos[a], coos[b], coos):
      continue
    area = calcArea(coos[a], coos[b])
    maxarea = max(maxarea, area)
    # drawtile(coos, (coos[a], coos[b]))
    # print(coos[a], coos[b], area)
  return maxarea

