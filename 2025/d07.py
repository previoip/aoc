from functools import cache

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


def part2(inp):
  sequence = list(itersequence(inp))
  tachyons = list(map(lambda s: list(get_tachyons(s)), sequence[1:]))
  levels = len(tachyons)
  caches = dict()

  def scantree(beam, lv):
    key = (beam, lv)
    if key in caches:
      # print('from cached', key)
      return caches[key]
  
    retv = None
    if lv >= levels:
      retv = 1
    elif beam in tachyons[lv]:
      retv = 0
      retv += scantree(beam+1, lv+1)
      retv += scantree(beam-1, lv+1)
    else:
      retv = scantree(beam, lv+1)
    caches[key] = retv
    return retv

  return scantree(sequence[0].index('S'), 0)
