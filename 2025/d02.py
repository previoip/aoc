
def parse_ranges(instr):
  ranges = instr.split(',')
  for subrange in ranges:
    yield tuple(map(int, subrange.split('-')))

def validate_mirroring(product_id):
  product_id = str(product_id)
  ndigit = len(product_id)
  if (ndigit % 2 != 0) or (ndigit == 1): return True
  nlength = ndigit // 2
  return product_id[:nlength] != product_id[nlength:nlength*2]
  

def validate_repeating(product_id):
  product_id = str(product_id)
  ndigit = len(product_id)
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

  for line in sys.stdin:
    print('part1:', part1(line.strip()))
    print('part2:', part2(line.strip()))
