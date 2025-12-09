from shared.intops import uilog10, uisplit


def parse(inp):
  for v in inp.strip().split(' '):
    yield int(v)


blink_cache = dict()

def blink(stone, n):
  key = (stone, n)
  if key in blink_cache:
    return blink_cache[key]

  retv = 0
  if n <= 0:
    retv = 1
  else:
    ndigit = uilog10(stone)
    if stone == 0:
      retv = blink(1, n-1)
    elif ndigit % 2 == 0:
      s0, s1 = uisplit(stone, ndigit//2)
      retv += blink(s0, n-1)
      retv += blink(s1, n-1)
    else:
      retv += blink(stone*2024, n-1)
  blink_cache[key] = retv
  return retv
    


def part1(inp):
  print(inp)
  sums = 0
  for stone in parse(inp):
    sums += blink(stone, 25)
  return sums


def part2(inp):
  print(inp)
  sums = 0
  for stone in parse(inp):
    sums += blink(stone, 75)
  return sums
