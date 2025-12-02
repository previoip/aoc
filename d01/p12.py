
def parser(line):
  return int(line[1:]) * (-1 if line[0]=='L' else 1)

def part1(instr):
  dial_abs = 50
  count = 0
  for rot in instr:
    dial_abs += rot
    if dial_abs % 100 == 0: count += 1
    # print(rot, dial_abs, count, sep='\t')
  return count

def part2(instr):
  dial_abs = 50
  fullrot_tt = [0, 0]
  count = 0
  for rot in instr:
    dial_abs += rot
    fullrot_tt[0] = fullrot_tt[1]
    fullrot_tt[1] = dial_abs // 100
    count += abs(fullrot_tt[1]-fullrot_tt[0])
    # print(rot, dial_abs, fullrot_tt[1]-fullrot_tt[0], count, sep='\t')
  return count

if __name__ == '__main__':
  import sys

  instr = list()
  for line in sys.stdin:
    instr.append(parser(line.strip()))

  print('ans part1', part1(instr))
  print('ans part2', part2(instr))
