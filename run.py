import sys, os

def module_from_file(module_name, file_path):
  import importlib.util
  spec = importlib.util.spec_from_file_location(module_name, file_path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

def init_argparser():
  from argparse import ArgumentParser
  parser = ArgumentParser(prog='aoc')
  parser.add_argument('modulepath')
  parser.add_argument('function')
  parser.add_argument('-i', '--input', type=str, help='fetch input string from arg')
  parser.add_argument('-f', '--file', type=str, help='fetch input from file')
  parser.add_argument('-p', '--pipe', action='store_true', help='fetch input from pipe')
  parser.add_argument('-a', '--all', action='store_true', help='multiline input')
  return parser

def validate_modulepath(path):
  pwd = os.path.dirname(os.path.abspath(__file__))
  path = os.path.abspath(path)
  return os.path.commonpath((pwd, path)) == pwd


if __name__ == '__main__':
  parser = init_argparser()
  args = parser.parse_args()

  if not validate_modulepath(args.modulepath):
    raise RuntimeError('import from outside this directory is not allowed')

  if not os.path.exists(args.modulepath):
    raise FileNotFoundError(f'cannot locate module {args.modulepath}')

  module = module_from_file('puzzle', args.modulepath)
  if not hasattr(module, args.function):
    attrs = filter(lambda s: not s.startswith('_') and callable(getattr(module, s)), dir(module))
    raise AttributeError(f'module has no attribute "{args.function}"\naccessible callable attributes:\n\t{"\n\t".join(attrs)}')

  if args.function.startswith('_'):
    raise AttributeError('target module attribute is a private member')

  function = getattr(module, args.function)
  def runfunc(inp):
    print()
    print(args.function + ':')
    print(function(inp))

  if not args.input is None:
    if args.all:
      runfunc(args.input)
    else:
      for line in args.input.splitlines():
        runfunc(line)

  if not args.file is None:
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
      raise FileNotFoundError(f'cannot locate file {args.file}')
    with open(args.file, 'r') as fp:
      if args.all:
        runfunc(fp.read())
      else:
        for line in fp.readlines():
          runfunc(line)

  if args.pipe:
    if sys.stdin.isatty():
      raise RuntimeError('pipe is not open')
    if args.all:
      runfunc(sys.stdin.read())
    else:
      for line in sys.stdin:
        runfunc(line)
