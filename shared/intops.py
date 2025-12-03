
def uilog10(n):
  # floor(log10(n))
  n = abs(n)
  i = 0
  while n-10**i >= 0:
    i += 1
  return i

def uitrr(n, l):
  # uint trim right
  return n // (10**l)

def uitrl(n, l):
  # uint trim left
  p = 10**(uilog10(n)-l)
  return n - n // p * p

def uisplice(n, offset, length):
  # uint splice
  n = uitrl(n, offset)
  ndigit = uilog10(n)
  return uitrr(n, ndigit-length)
