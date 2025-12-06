def parser(inp):
  res = list()
  for line in inp.splitlines():
    res.append(line.strip())
  return res  

def argmax(arr, inv=False, offset=None):
  n = len(arr)
  cmp = 0
  idx = 0
  for i in range(n):
    if not offset is None:
      if inv and i > len(arr)-offset: continue
      if i < offset: continue
    if inv: i = n-i-1
    if cmp < arr[i]:
      cmp = arr[i]
      idx = i
  return idx


def part1(inp):
  jolts = parser(inp.strip())
  sums = 0
  for jolt in jolts:
    jolt = list(map(int, jolt))
    i = argmax(jolt[:-1])
    j = argmax(jolt[i+1:], True)
    m = jolt[:-1][i]
    n = jolt[i+1:][j]
    sums += m*10+n
  return sums


def parsejolt(jolt, scores):
  retv = ''
  for i, s in enumerate(scores):
    if s == -1:
      retv += jolt[i]
  return int(retv)

def solve_indices(jolt, numdigit):
  digits = len(jolt)
  scores = list(map(ord, jolt))
  switch = False
  offset = 0
  for n in range(numdigit):
    i = argmax(scores, switch, offset)
    scores[i] = -1
    if not switch:
      offset = i
    print(jolt, scores, parsejolt(jolt, scores))
    if offset >= digits-2:
      switch = True
      offset = 0
      print('switched')

  res = parsejolt(jolt, scores)
  print('>>', jolt)
  print('>>', scores)
  print('>>', res)
  raise RuntimeError
  return res


def solve_naive(jolt, numdigit):
  largest = 0
  tempind = 0
  ndigits = len(jolt)
  ascores = [0 for _ in range(ndigits)]
  for n in range(numdigit):
    for m in range(ndigits):
      if ascores[m] == -1: continue
      ascores[m] = -1
      num = parsejolt(jolt, ascores)
      if num > largest:
        largest = num
        tempind = m
      ascores[m] = 0
    ascores[tempind] = -1
  return parsejolt(jolt, ascores)

def part2(inp):
  jolts = parser(inp.strip())
  sums = 0
  for jolt in jolts:
    sums += solve_naive(jolt, 12)
  return sums
