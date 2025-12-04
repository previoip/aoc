import sys
from itertools import product

class GridIndexer:

  class E_RTSTRIDE:
    rt    = ( 1, 0)
    dw_rt = ( 1, 1)
    dw    = ( 0, 1)
    dw_lf = (-1, 1)
    lf    = (-1, 0)
    up_lf = (-1,-1)
    up    = ( 0,-1)
    up_rt = ( 1,-1)

    east  = ( 1, 0)
    seast = ( 1, 1)
    south = ( 0, 1)
    swest = (-1, 1)
    west  = (-1, 0)
    nwest = (-1,-1)
    north = ( 0,-1)
    neast = ( 1,-1)

  def __init__(self, w, h):
    self.w = w
    self.h = h
    self.N = w * h

  def itox(self, i):
    return i % self.w
  
  def itoy(self, i):
    return i // self.w

  def itoc(self, i):
    return self.itox(i), self.itoy(i)

  def xytoi(self, x, y, wrap=False):
    if wrap:
      x %= self.w
      y %= self.h
    else:
      if self.isoobxy(x, y):
        return -1
    return x + self.w * y

  def ctoi(self, c):
    return self.xytoi(c[0], c[1])

  def iterc(self):
    for i in range(self.N):
      yield self.itoc(i)

  def wrapxy(self, x, y):
    return x%self.w, y%self.h

  def wrapc(self, c):
    return self.wrapxy(c[0], c[1])

  def isoobxy(self, x, y):
    return x < 0 \
    or x >= self.w \
    or y < 0 \
    or y >= self.h
  
  def isoobc(self, c):
    return self.isoobxy(c[0], c[1])

  def iterraytracexy(self, x, y, stride: E_RTSTRIDE = (1,0)):
    ox, oy = stride
    if (ox==0) and (oy==0): raise ValueError('stride offset cannot be zero')
    for _ in range(sys.maxsize):
      yield x, y
      x += ox
      y += oy
      if self.isoobxy(x, y): break

  def iterraytracei(self, x, y, stride: E_RTSTRIDE = (1,0)):
    for x, y in self.iterraytracexy(x, y, stride):
      yield self.xytoi(x, y)

  def itersquarekernelxy(self, x, y, size, wrap=False):
    m = size//2
    for ox, oy in product(range(size), range(size)):
      dx = x+ox-m
      dy = y+oy-m
      if wrap:
        dx %= self.w
        dy %= self.h
      yield (ox, oy), (dx, dy)

  def itersquarekerneli(self, x, y, size, wrap=False):
    for (ox, oy), (x, y) in self.itersquarekernelxy(x, y, size, wrap):
      yield (ox, oy), self.xytoi(x, y, wrap)


if __name__ == '__main__':
  import numpy as np
  a = np.arange(25)
  ar = a.reshape(5,5)
  indexer = GridIndexer(5,5)

  print(ar)

  for stride in [
    GridIndexer.E_RTSTRIDE.east,
    GridIndexer.E_RTSTRIDE.seast,
    GridIndexer.E_RTSTRIDE.south,
    GridIndexer.E_RTSTRIDE.swest,
    GridIndexer.E_RTSTRIDE.west,
    GridIndexer.E_RTSTRIDE.nwest,
    GridIndexer.E_RTSTRIDE.north,
    GridIndexer.E_RTSTRIDE.neast,
  ]:
    indices = list(indexer.iterraytracei(2,2,stride))
    print(a[indices], stride)

  print()
  kernel = np.zeros((3,3))
  for (x, y), i in indexer.itersquarekerneli(0, 0, 3):
    kernel[y, x] = a[i]
  print(kernel)

  for (x, y), (dx, dy) in indexer.itersquarekernelxy(0, 0, 3, wrap=False):
    kernel[y, x] = ar[dy][dx]
    print((x, y), (dx, dy))
  print(kernel)