def parser(inp):
  res = list()
  for line in inp.splitlines():
    res.append(list(map(int, line.strip())))
  return res  

def argmax(arr, reversed=False):
  l = len(arr)
  j = 0
  v = 0
  for i in range(len(arr)):
    if reversed:
      i = l-i-1
    if arr[i] > v:
      v = arr[i]
      j = i
  return j

def part1(inp):
  jolts = parser(inp.strip())
  sums = 0
  for jolt in jolts:
    i = argmax(jolt[:-1])
    j = argmax(jolt[i+1:], True)
    m = jolt[:-1][i]
    n = jolt[i+1:][j]
    sums += m*10+n
  return sums
