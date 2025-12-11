import sqlite3
import os
from threading import Lock

def sqlite3w_classmethod_closedconn_fallback_value(value):
  def decorator(func):
    def methodwrapper(self, *args, **kwargs):
      if self._isclosed:
        return value
      try:
        retv = func(self, *args, **kwargs)
      except sqlite3.ProgrammingError:
        print('warning: connection closed but flag is unset')
        self._isclosed = True
        retv = value
      return retv
    return methodwrapper
  return decorator

class _SqlLite3TempConn:
  _instances = list()
  _thread_lock = Lock()

  @classmethod
  def _handle_closeAllOpenConnInstance(cls, *_, **__):
    for inst in cls._instances:
      inst.close()

  def __init__(self, path, preserve=False, **sqlite3_connect_kwargs):
    self._path = path
    self._isclosed = False
    self._preserve = preserve
    self._conn = sqlite3.connect(path, **sqlite3_connect_kwargs)
    self._cur0 = self._conn.cursor()
    self._instances.append(self)

  def __repr__(self):
    return f'<sqlite3:{hex(id(self))}[{self._path}]>'

  def close(self):
    self._thread_lock.acquire()
    if self._isclosed:
      if self in self._instances:
        self._instances.remove(self)
      self._thread_lock.release()
      return
    print(f'closing conn: {self}')
    self._conn.commit()
    self._conn.close()
    self._isclosed = True
    if not self._preserve and os.path.exists(self._path):
      # !!!
      os.unlink(self._path)
    if self in self._instances:
      self._instances.remove(self)
    self._thread_lock.release()


class SqlLite3Deque(_SqlLite3TempConn):

  def __init__(self, path, preserve=False, **sqlite3_connect_kwargs):
    super().__init__(path, preserve=preserve, **sqlite3_connect_kwargs)
    self._conn.execute("""
    create table if not exists Deque (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      data BLOB,
      _ones INTEGER DEFAULT 1
    )
    """)

  @staticmethod
  def serializer(item):
    return item
  
  @staticmethod
  def deserializer(blob):
    return blob

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def _get_first_id(self):
    query = self._cur0.execute('select min(id) from Deque')
    return query.fetchone()[0]

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def _get_last_id(self):
    query = self._cur0.execute('select max(id) from Deque')
    return query.fetchone()[0]

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def put(self, item):
    self._cur0.execute('insert into Deque (data) values (?)', (self.serializer(item),))
    self._conn.commit()

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def append(self, item):
    self.put(item)

  @sqlite3w_classmethod_closedconn_fallback_value(False)
  def has(self, item):
    query = self._cur0.execute('select id from Deque where data=(?)', (self.serializer(item),))
    return not query.fetchone() is None

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def _fetch_from_id(self, _id):
    query = self._cur0.execute(f'select data from Deque where id={_id}')
    blob, = query.fetchone()
    self._cur0.execute(f'delete from Deque where id={_id}')
    self._conn.commit()
    return blob

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def get(self):
    last_id = self._get_last_id()
    if last_id is None:
      return None
    blob = self._fetch_from_id(last_id)
    return self.deserializer(blob)

  @sqlite3w_classmethod_closedconn_fallback_value(None)
  def get_left(self):
    last_id = self._get_first_id()
    if last_id is None:
      return None
    blob = self._fetch_from_id(last_id)
    return self.deserializer(blob)

  def pop(self):
    return self.get()

  def popleft(self):
    return self.get_left()

  def empty(self):
    return self._get_last_id() is None

  def count(self):
    if self.empty():
      return 0
    query = self._cur0.execute('select sum(_ones) from Deque')
    return query.fetchone()[0]

  def __len__(self):
    return self.count()

# backward compat
SqlLite3Queue = SqlLite3Deque

import signal, atexit
signal.signal(signal.SIGTERM, _SqlLite3TempConn._handle_closeAllOpenConnInstance)
signal.signal(signal.SIGINT, _SqlLite3TempConn._handle_closeAllOpenConnInstance)
atexit.register(_SqlLite3TempConn._handle_closeAllOpenConnInstance)
