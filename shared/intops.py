
def tenthpower(n):
  # floor-log10
  n = abs(n)
  i = 0
  while n-10**i >= 0:
    i += 1
  return i

def uirtr(n, l):
  # uint trim right
  return n // (10**l)

def uiltr(n, l):
  # uint trim left
  p = 10**(tenthpower(n)-l)
  return n - n // p * p

def uisplice(n, offset, length):
  # uint splice
  n = uiltr(n, offset)
  ndigit = tenthpower(n)
  return uirtr(n, ndigit-length)
