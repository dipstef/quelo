from contextlib import closing

from pysqlite2 import dbapi2 as sqlite3

from ..statement import ExecuteScript, Commit, Execute, Select, IterateSelect, CloseCursor


def connect_db(path):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    return conn


class DbConnection(closing):

    def __init__(self):
        super(DbConnection, self).__init__(self)

    def execute_script(self, script):
        self._execute(ExecuteScript(script))

    def commit(self):
        self._execute(Commit())

    def _execute(self, statement):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class DbFile(DbConnection):

    def __init__(self, path):
        super(DbFile, self).__init__()
        self._conn = connect_db(path)

    def cursor(self):
        return DbCursor(self._conn.cursor())

    def close(self):
        self._conn.close()

    def _execute(self, statement):
        return statement(self._conn)


class DbCursor(closing):

    def __init__(self, cursor):
        super(DbCursor, self).__init__(self)
        self._cursor = cursor

    def execute(self, query, args=None):
        return self._execute(Execute(query, args))

    def select(self, query, args=None):
        return self._execute(Select(query, args))

    def iterate_select(self, query, args=None, result_size=100):
        return self._execute(IterateSelect(query, args, result_size=result_size))

    def close(self):
        return self._execute(CloseCursor())

    def _execute(self, statement):
        return statement(self._cursor)