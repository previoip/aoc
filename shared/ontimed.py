from time import time

class OnTimelapsed:
  @staticmethod
  def strftime(sec):
    m = int(sec) // 60
    h = m // 60
    m %= 60
    sec %= 60
    return f'{h: 4d}:{m:02d}:{sec:05.02f}'

  def __init__(self):
    self._tdelta = 0
    self._tglobal = time()
    self._tstamp = time()
    self._tsums = 0

  def _capture(self):
    timestamp = time()
    self._tdelta = timestamp - self._tstamp
    self._tstamp = timestamp
    self._tsums += self._tdelta

  def getts(self):
    return self._tstamp - self._tglobal
  
  def _ckssums(self, sec):
    if self._tsums > sec:
      self._tsums = 0
      return True
    return False

  def checkandrun(self, sec, func, *args, **kwargs):
    self._capture()
    if self._ckssums(sec):
      return func(*args, **kwargs)
    return None

  def checkandprint(self, sec, *args, **kwargs):
    self._capture()
    if self._ckssums(sec):
      print(f'{self.strftime(self.getts())}', *args, **kwargs)
