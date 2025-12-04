import sqlite3


class SqlLite3Queue:
  _instances = list()

  def __init__(self, path):
    self._instances.append(self)
    self._isclosed = False
    self._conn = sqlite3.connect(path)
    self._conn.execute("""
    create table if not exists Queue (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      data BLOB
    )
    """)
    self._cur0 = self._conn.cursor()

  def close(self):
    if self._isclosed:
      return
    print(f'closing conn: {self}')
    self._conn.commit()
    self._conn.close()
    self._isclosed = True

  @staticmethod
  def serializer(item):
    return item
  
  @staticmethod
  def deserializer(blob):
    return blob

  def _get_last_id(self):
    query = self._cur0.execute('select max(id) from Queue')
    return query.fetchone()[0]

  def put(self, item):
    self._cur0.execute('insert into Queue (data) values (?)', (self.serializer(item),))
    self._conn.commit()

  def get(self):
    last_id = self._get_last_id()
    if last_id is None:
      return None
    query = self._cur0.execute(f'select data from Queue where id={last_id}')
    blob, = query.fetchone()
    self._cur0.execute(f'delete from Queue where id={last_id}')
    self._conn.commit()
    return self.deserializer(blob)

  def empty(self):
    return self._get_last_id() is None


import signal, atexit
def _sqlite3w_SqlLite3Queue_handle_closeall(*args, **kwargs):
  for instance in SqlLite3Queue._instances:
    instance.close()
signal.signal(signal.SIGTERM, _sqlite3w_SqlLite3Queue_handle_closeall)
signal.signal(signal.SIGINT, _sqlite3w_SqlLite3Queue_handle_closeall)
atexit.register(_sqlite3w_SqlLite3Queue_handle_closeall)
