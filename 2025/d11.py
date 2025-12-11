from collections import defaultdict

def getlkups(lkups, value):
  if not value in lkups:
    lkups.append(value)
  return lkups.index(value)

def parser(inp):
  nodes = defaultdict(list)
  lkups = list()
  for line in inp.splitlines():
    node = line[:3]
    node = getlkups(lkups, node)
    for conn in line[4:].split():
      conn = getlkups(lkups, conn)  
      nodes[node].append(conn)
  return lkups, dict(nodes)

def part1(inp):
  lkups, nodes = parser(inp)
  start = getlkups(lkups, 'you')
  goal = getlkups(lkups, 'out')

  queue = list()
  queue.append((start, [start]))
  loop = True
  valid_paths = list()
  while loop and queue:
    node, visited = queue.pop(0)
    conns = nodes[node]
    for conn in conns:
      if conn == goal:
        valid_paths.append([*visited, conn])
      elif conn in visited:
        continue
      else:
        queue.append((conn, [*visited, conn]))
  # for path in valid_paths:
  #   print([lkups[i] for i in path])
  return len(valid_paths)

def part2(inp):
  lkups, nodes = parser(inp)
  svr = getlkups(lkups, 'svr')
  dac = getlkups(lkups, 'dac')
  fft = getlkups(lkups, 'fft')
  goal = getlkups(lkups, 'out')

  queue = list()
  queue.append((svr, [svr]))
  loop = True
  valid_paths = list()
  cached = list()
  while loop and queue:
    node, visited = queue.pop(0)
    conns = nodes[node]
    for conn in conns:
      if conn == goal:
        valid_paths.append([*visited, conn])
      elif conn in visited:
        continue
      elif [*visited, conn] in cached:
        continue
      else:
        checked = [*visited, conn]
        cached.append(checked)
        queue.append((conn, checked))

  counter = 0
  for path in valid_paths:
    if fft in path and dac in path:
      counter += 1
      # print([lkups[i] for i in path])
  return counter
