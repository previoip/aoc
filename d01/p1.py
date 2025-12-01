
class config:
  input_p1 = './d01/in_p1.txt'
  input_p1_test = './d01/in_p1_test.txt'

def read_rot_instr(path):
  def parser(line):
    return int(line[1:]) * (-1 if line[0]=='L' else 1)
  with open(path, 'r') as fp:
    for line in fp.readlines():
      yield parser(line.strip())

def part1(input_path):
  dial_abs = 50
  count = 0
  for rot in read_rot_instr(input_path):
    dial_abs += rot
    if dial_abs % 100 == 0: count += 1
    # print(rot, dial_abs, count, sep='\t')
  print('pwd', count)

def part2(input_path):
  dial_abs = 50
  fullrot_tt = [0, 0]
  count = 0
  for rot in read_rot_instr(input_path):
    dial_abs += rot
    fullrot_tt[0] = fullrot_tt[1]
    fullrot_tt[1] = dial_abs // 100
    count += abs(fullrot_tt[1]-fullrot_tt[0])
    # print(rot, dial_abs, fullrot_tt[1]-fullrot_tt[0], count, sep='\t')

  print('pwd', count)

if __name__ == '__main__':
  print('\npart1 test')
  part1(config.input_p1_test)
  print('\npart1')
  part1(config.input_p1)
  print('\npart2 test')
  part2(config.input_p1_test)
  print('\npart2')
  part2(config.input_p1)


