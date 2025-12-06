
def parser(inp):
  idranges = list()
  items = list()
  switch = False
  for line in inp.splitlines():
    line.strip()
    if not line: 
      switch = True
      continue
    if switch:
      items.append(int(line))
    else:
      idranges.append(tuple(map(int, line.split('-'))))
  return idranges, items

def inrange(v, lo, hi):
  return v >= lo and v <= hi


def part1(inp):
  ranges, items = parser(inp)
  counter = 0
  for item in items:
    for lo, hi in ranges:
      if inrange(item, lo, hi):
        counter += 1
        break
  return counter


def defrag(rangea, rangeb):
    la, ha = rangea
    lb, hb = rangeb
    la_b = inrange(la, lb, hb)
    ha_b = inrange(ha, lb, hb)
    lb_a = inrange(lb, la, ha)
    hb_a = inrange(hb, la, ha)

    # AAAA
    #      BBBB
    # ----or----
    #      AAAA
    # BBBB
    if not la_b \
    and not ha_b \
    and not lb_a \
    and not hb_a:
      return None
  
    # AAAAAAA
    #      BBBB
    if not la_b \
    and ha_b \
    and lb_a \
    and not hb_a:
      return (la, hb)


    #   AAAAAAA
    # BBBBB
    if la_b \
    and not ha_b \
    and not lb_a \
    and hb_a:
      return (lb, ha)

    # AAAAAAAA
    #   BBBB
    if lb_a \
    and hb_a:
      return (la, ha)

    #   AAAA
    # BBBBBBBB
    if la_b \
    and ha_b:
      return (lb, hb)

    #  AAAAAA
    #  BBBBBB
    if la == lb \
    and ha == hb:
      # return (la, ha)
      return None

    raise ValueError(f'condition not defined: {rangea} {rangeb}')


def defragtwinning(rangea, rangeb):
  res = defrag(rangea, rangeb)
  if res is None:
    res = defrag(rangeb, rangea)
  return res


def part2(inp):
  chunks, _ = parser(inp)
  length = len(chunks)
  ckptln = length
  cura = 0
  curb = 0

  for _ in range(10_000_000):

    cura += 1
    if cura == curb:
      continue
    if cura % length == 0:
      cura = 0
      curb += 1
    if curb !=0 and curb % length == 0:
      cura = 0
      curb = 0
  
      if ckptln == length: break
      ckptln = length

    cura %= length
    curb %= length

    rnga = chunks[cura]
    rngb = chunks[curb]
    frag = defragtwinning(rnga, rngb)
    if not frag is None:
      chunks[cura] = None
      chunks[curb] = None
      while None in chunks:
        chunks.remove(None)
      chunks.append(frag)
      # print('defragged:', rnga, rngb, '=>', frag)
      length = len(chunks)
  else:
    print('warning: loop exhausted before completion')
  
  sums = 0
  for l, h in sorted(chunks):
    sums += h-l+1

  return sums
