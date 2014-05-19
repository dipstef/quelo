from unicoder import encoded

from .sqlite.execute import Sqlite3Statement


class ConnectionStatement(Sqlite3Statement):

    def _execute_statement(self, conn):
        raise NotImplementedError


class Cursor(ConnectionStatement):

    def _execute_statement(self, conn):
        return conn.cursor()

    def __str__(self):
        return 'conn.cursor()'


class Commit(ConnectionStatement):

    def _execute_statement(self, conn):
        conn.commit()

    def __str__(self):
        return 'commit()'


class ExecuteScript(ConnectionStatement):

    def __init__(self, script):
        self._script = script

    def _execute_statement(self, conn):
        conn.executescript(self._script)

    def __str__(self):
        return encoded(unicode(self))

    def __unicode__(self):
        class_name = self.__class__.__name__
        return u'%s:\n%s ' % (class_name, ''.rjust(len(class_name) + 1) + self._script)

    def __repr__(self):
        return self.__str__()


class CursorStatement(Sqlite3Statement):

    def _execute_statement(self, cursor):
        return self._cursor_statement(cursor)

    def _cursor_statement(self, cursor):
        raise NotImplementedError


class CloseCursor(CursorStatement):

    def _cursor_statement(self, cursor):
        cursor.close()

    def __str__(self):
        return 'cursor.close()'


class Execute(CursorStatement):

    def __init__(self, query, args):
        self._query = query
        self._args = args or ()

    def _cursor_statement(self, cursor):
        cursor.execute(self._query, self._args)

    def __str__(self):
        return encoded(unicode(self))

    def __unicode__(self):
        class_name = self.__class__.__name__
        args = unicode(self._args) if self._args else ''

        return u'%s:\n%s %s' % (class_name, ''.rjust(len(class_name) + 1) + self._query, u': %s' % args)

    def __repr__(self):
        return self.__str__()


class Select(Execute):

    def __init__(self, query, args):
        super(Select, self).__init__(query, args)

    def _cursor_statement(self, cursor):
        cursor.execute(self._query, self._args)
        rows = cursor.fetchall()
        return rows


class IterateSelect(Execute):

    def __init__(self, query, args, result_size=100):
        super(IterateSelect, self).__init__(query, args)
        self._result_size = result_size

    def _cursor_statement(self, cursor):
        cursor.execute(self._query, self._args)

        while True:
            results = cursor.fetchmany(self._result_size)
            if not results:
                break
            for result in results:
                yield result