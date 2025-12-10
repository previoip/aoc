def itob(uints):
  r = 0
  for i in uints:
    r |= 1 << i
  return r

def flipm(a, b):
  return a^b

def lighttob(s):
  r = 0
  for i in range(len(s)):
    if s[i] == '#':
      r ^= 1 << i
  return r

def parser(inp):
  for line in inp.splitlines():
    goal, _, instr = line.partition(' ')
    wirings, _, jolts = instr.rpartition(' ')
    wirings = list(map(lambda s: tuple(map(int, s[1:-1].split(','))), wirings.split(' ')))
    jolts = list(map(int, jolts[1:-1].split(',')))
    yield goal, wirings, jolts

def part1(inp):
  sums = 0
  total = 0
  for i in parser(inp): total += 1

  for i, (goal, wirings, _) in enumerate(parser(inp)):
    goal = lighttob(goal[1:-1])
    wirings = list(map(itob, wirings))
    deque = list()
    deque.append((0, 0))

    depth = 0
    loop = True
    traversed = list()
    while loop and deque:
      b, d = deque.pop(0)
      for schema in wirings:
        bt = b ^ schema
        if bt in traversed:
          continue
        traversed.append(bt)
        if bt == goal:
          loop = False
          depth = d+1
          break
        deque.append((bt, d+1))
    sums += depth
    print(f'{i+1: 3d}/{total}', depth)
  return sums

def part2(inp):
  sums = 0
  total = 0
  for i in parser(inp): total += 1

  for i, (goal, wirings, jolt) in enumerate(parser(inp)):
    print(goal, wirings, jolt)
    goal = lighttob(goal[1:-1])
    deque = list()
    deque.append((0, 0, jolt))

    depth = 0
    loop = True
    traversed = list()
    while loop and deque:
      b, d, joltc = deque.pop(0)
      for schema in wirings:
        joltd = joltc.copy()
        for k in schema:
          joltd[k] -= 1
        if any(map(lambda k: k<0, joltd)):
          continue
        bt = b ^ itob(schema)
        key = (bt, joltd.copy())
        if key in traversed:
          continue
        traversed.append(key)
        if bt == goal and all(map(lambda k: k==0, joltd)):
          loop = False
          depth = d+1
          break
        deque.append((bt, d+1, joltd))
    sums += depth
    print(f'{i+1: 3d}/{total}', depth)
  return sums
