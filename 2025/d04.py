from shared.grid import GridIndexer


def fetch_removable_papers(grid):
  nrow = len(grid)
  ncol = len(grid[0])
  kernelarr = [None for _ in range(9)]
  indexer = GridIndexer(nrow, ncol)
  accessible = list()
  for y in range(nrow):
    for x in range(ncol):
      if grid[y][x] != '@': continue
      for i, (_, (ix, iy)) in enumerate(indexer.itersquarekernelxy(x, y, 3)):
        if indexer.isoobxy(ix, iy):
          kernelarr[i] = '.'
        else:
          kernelarr[i] = grid[iy][ix]
      rollcount = kernelarr.count('@')
      if rollcount > 0 and rollcount <= 4:
        accessible.append((x, y))
  return accessible

def grid_repl(grid, items, repl):
  new_grid = list()  
  nrow = len(grid)
  ncol = len(grid[0])
  for y in range(nrow):
    new_grid.append(list())
    for x in range(ncol):
      new_grid[y].append(grid[y][x])
  for x, y in items:
    new_grid[y][x] = repl
  for y in range(nrow):
    new_grid[y] = ''.join(new_grid[y])
  return new_grid

def part1(inp: str):
  grid = inp.splitlines()
  items = fetch_removable_papers(grid)

  print('\n'.join(grid))
  print()
  print('\n'.join(grid_repl(grid, items, 'X')))
  print()

  return len(items)

def part2(inp: str):
  grid = inp.splitlines()
  items = fetch_removable_papers(grid)
  sums = 0
  while True:
    items = fetch_removable_papers(grid)
    if len(items) == 0: break
    sums += len(items)
    grid = grid_repl(grid, items, '.')
  return sums

