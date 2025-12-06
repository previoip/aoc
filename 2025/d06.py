
def parseinstr(inp):
  lines = inp.splitlines()
  oprs = lines[-1]
  j = 0
  for i in range(len(oprs)):
    if i != 0 and oprs[i] != ' ':
      yield [lines[k][j:i] for k in range(len(lines))]
      j = i
  i = len(oprs)
  yield [lines[k][j:i] for k in range(len(lines))]

def part1(inp):
  sums = 0
  for instr in parseinstr(inp):
    opr = instr.pop(-1).strip()
    tmp = int(instr.pop())
    for num in instr:
      if opr == '*':
        tmp *= int(num)
      elif opr == '+':
        tmp += int(num)
      else: raise ValueError
    sums += tmp
  return sums

def transpose(ls):
  nrow = len(ls)
  ncol = len(ls[0])

  nls = list()
  for i in range(ncol):
    nls.append('')
    for j in range(nrow):
      nls[-1] += ls[j][i]
  return nls

def part2(inp):
  sums = 0
  for instr in parseinstr(inp):
    opr = instr.pop(-1).strip()
    instr = transpose(instr)
    instr = [int(i) for i in instr if i.strip()]
    tmp = instr.pop()
    for num in instr:
      if opr == '*':
        tmp *= num
      elif opr == '+':
        tmp += num
      else: raise ValueError
    sums += tmp
  return sums
