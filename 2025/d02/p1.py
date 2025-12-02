from functools import cache

def parse_ranges(instr):
  ranges = instr.split(',')
  for subrange in ranges:
    yield tuple(map(int, subrange.split('-')))

@cache
def tenthpower(n):
  n = abs(n)
  i = 0
  while n-10**i >= 0:
    i += 1
  return i

def uirtr(n, l):
  return n // (10**l)

def uiltr(n, l):
  p = 10**(tenthpower(n)-l)
  return n - n // p * p

def uisplice(n, offset, length):
  n = uiltr(n, offset)
  ndigit = tenthpower(n)
  return uirtr(n, ndigit-length)

def validate_mirroring(product_id):
  product_id = str(product_id)
  ndigit = len(product_id)
  if (ndigit % 2 != 0) or (ndigit == 1): return True
  nlength = ndigit // 2
  return product_id[:nlength] != product_id[nlength:nlength*2]
  

def validate_repeating(product_id):
  product_id = str(product_id)
  ndigit = len(product_id)
  # if ndigit % 2 != 0:
  #   if ndigit == 1:
  #     return True
  #   char = product_id[0]
  #   for char_i in product_id[1:]:
  #     if not char == char_i:
  #       return True
  #   return False
  nlength = ndigit // 2
  for length in range(nlength,0,-1):
    if ndigit%length != 0: continue
    nstride = ndigit // length
    pattern = product_id[:length]
    stopflag = True
    # print(product_id, pattern, 'length', length, 'nstride', nstride)
    for stride in range(nstride):
      offset = length*stride
      substr = product_id[offset:offset+length]
      stopflag &= substr == pattern
      # print('', stride, offset, f'{substr} == {pattern}', stopflag)
    if stopflag: return False
  return True


def part1(instr):
  sums = 0
  for lo, hi in parse_ranges(instr):
    for product_id in range(lo, hi+1):
      if not validate_mirroring(product_id):
        sums += product_id
  return sums

def part2(instr):
  sums = 0
  for lo, hi in parse_ranges(instr):
    for product_id in range(lo, hi+1):
      if not validate_repeating(product_id):
        sums += product_id
  return sums


if __name__ == '__main__':
  import sys

  product_ids = list()
  for line in sys.stdin:
    # print('part1:', part1(line.strip()))
    print('part2:', part2(line.strip()))

