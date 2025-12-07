
def itersequence(inp):
  for line in inp.splitlines():
    if line.count('.') == len(line): continue
    yield line

def split_beams(i):
  yield i-1
  yield i+1

def get_tachyons(s):
  for i in range(len(s)):
    if s[i] == '^':
      yield i

def part1(inp):
  sequence = itersequence(inp)
  beams = set()
  beams.add(next(sequence).index('S'))
  counter = 0
  for row in sequence:
    tachs = set(get_tachyons(row))
    for tosplit in beams.intersection(tachs):
      counter += 1
      beams.remove(tosplit)
      for newbeam in split_beams(tosplit):
        beams.add(newbeam)
  return counter


from shared.ontimed import OnTimelapsed

def part2(inp):
  ckprint = OnTimelapsed()
  sequence = list(itersequence(inp))
  tachyons = list(map(lambda s: list(get_tachyons(s)), sequence[1:]))
  levels = len(tachyons)
  queue = list()
  queue.append((sequence[0].index('S'), 0))
  counter = 0
  while queue:
    ckprint.checkandprint(10, counter, len(queue))
    tup = queue.pop()
    beam, lv = tup
    if lv >= levels:
      counter +=1
      continue
    if beam in tachyons[lv]:
      for newbeam in split_beams(beam):
        queue.append((newbeam, lv+1))
    else:
      queue.append((beam, lv+1))
  return counter
