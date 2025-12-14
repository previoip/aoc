from shared.grid import GridIndexer

def swap(a, b):
  return b, a

def batchoffset(x, y, iterable):
  for dx, dy in iterable:
    yield x+dx, y+dy


class DotMatrix:
  @classmethod
  def fromstr(cls, s):
    lines = s.strip().splitlines()
    nrow = len(lines)
    ncol = len(lines[0])
    for line in lines:
      assert len(line) == ncol
    inst = cls(ncol, nrow)
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        if char == '#':
          inst.putdot(x, y)
    return inst

  @property
  def w(self):
    return self.idxr.w

  @property
  def h(self):
    return self.idxr.h

  def __repr__(self):
    lines = [['.' for _ in range(self.idxr.w)] for _ in range(self.idxr.h)]
    for x, y in self.dots:
      lines[y][x] = '#'
    for i, line in enumerate(lines):
      lines[i] = ''.join(line)
    return str(self.idxr.shape) + '\n' + '\n'.join(lines) + '\n'

  def __init__(self, w, h):
    self.idxr = GridIndexer(w, h)
    self.dots = set()

  def putdot(self, x, y):
    if self.idxr.isoobxy(x, y): raise IndexError('oob')
    self.dots.add((x, y))

  def hasdot(self, x, y):
    return (x, y) in self.dots

  def add(self, x, y, dotm):
    for dx, dy in dotm.dots:
      self.putdot(x+dx, y+dy)

  def clear(self):
    self.dots.clear()

  def copy(self):
    inst = self.__class__(self.w, self.h)
    inst.dots = self.dots.copy()
    return inst

  def bool_intersect(self, x, y, dotm):
    inst = self.__class__(self.w, self.h)
    inst.dots = self.dots.intersection(batchoffset(x, y, dotm.dots))
    return inst

  def rotatecw(self, n):
    ssin = (1,1,-1,-1)
    scos = (1,-1,-1,1)
    osin = (0,0,1,1)
    ocos = (0,1,1,0)
    n %= 4
    if n==0: return
    iseve = n %2 == 0 
    if not iseve:
      self.idxr.w, self.idxr.h = swap(self.idxr.w, self.idxr.h)  
    new_dots = set()
    for x, y in self.dots:
      if not iseve:
        x, y = swap(x, y)
      x = x*scos[n]+ocos[n]*(self.idxr.w-1)
      y = y*ssin[n]+osin[n]*(self.idxr.h-1)
      new_dots.add((x, y))
    del self.dots
    self.dots = new_dots
    return self

def dotm_generate_rotsym(dotm):
  symmetries = [dotm]
  for i in range(1, 4):
    perm = dotm.copy().rotatecw(i)
    for sym in symmetries:
      if sym.dots == perm.dots:
        break
    else:
      symmetries.append(perm)
  return symmetries


def parser(inp):
  perms = list()
  areas = list()
  chunks = inp.split('\n\n')
  for instr in chunks.pop().splitlines():
    size, _, counts = instr.partition(':')
    size = size.split('x')
    size = (int(size[0]), int(size[1]))
    counts = tuple(map(int, counts.strip().split(' ')))
    areas.append((DotMatrix(*size), counts))
  for chunk in chunks:
    _, _, shape = chunk.partition(':')
    perms.append(dotm_generate_rotsym(DotMatrix.fromstr(shape)))
  return perms, areas


def part1(inp):
  shapespermute, areas = parser(inp)

  for shapes in shapespermute:
    for shape in shapes:
      print(shape)
    print('-'*20)

  for region, counts in areas:
    print(counts)
    print(region)
    print()

  raise NotImplementedError
