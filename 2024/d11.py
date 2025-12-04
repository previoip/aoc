from shared.intops import uilog10, uisplit
from queue import Queue

def parse(inp):
  for v in inp.strip().split(' '):
    yield (0, int(v))

def worker(states, queue, maxblink):
  item = queue.get()
  if item is None:
    return
  c, n = item
  if c >= maxblink:
    states['sums'] += 1
  else:
    c += 1
    ndigit = uilog10(n)
    if n == 0:
      queue.put((c, 1))
    elif ndigit % 2 == 0:
      n0, n1 = uisplit(n, ndigit//2)
      queue.put((c, n0))
      queue.put((c, n1))
    else:
      queue.put((c, n*2024))  

def part1(inp):
  queue = Queue()
  states = {'sums':0}
  for c, t in parse(inp):
    queue.put((c, t))
  while not queue.empty():
    worker(states, queue, 25)
  return states

def part2(inp):
  queue = Queue()
  states = {'sums':0}
  for c, t in parse(inp):
    queue.put((c, t))
  while not queue.empty():
    worker(states, queue, 75)
  return states
