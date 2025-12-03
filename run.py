import sys, os

ARG_OPTIONS_HELP = '<path-to-py> <funcname> [stdin]'

def module_from_file(module_name, file_path):
  import importlib.util
  spec = importlib.util.spec_from_file_location(module_name, file_path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module)
  return module

if __name__ == '__main__':
  if len(sys.argv) == 1:
    raise ValueError('inadequate args: ' + ARG_OPTIONS_HELP)

  path = sys.argv[1]
  if not os.path.exists(path):
    raise FileNotFoundError(f'cannot relocate module {path}: ')

  funcname = sys.argv[2]
  module = module_from_file('_module', path)
  if not hasattr(module, funcname):
    raise AttributeError(f'module has no attribute {funcname}: ' + ARG_OPTIONS_HELP)

  function = getattr(module, funcname)
  is_all = len(sys.argv) > 3 and sys.argv[3] == '--all'

  if not sys.stdin.isatty():
    if is_all:
      print(funcname, ':', function(sys.stdin.read()))
    else:
      for line in sys.stdin:
        print(funcname, ':', function(line))
  else:
    for line in sys.argv[3:]:
      print(funcname, ':', function(line))
