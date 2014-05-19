from pysqlite2 import dbapi2 as sqlite3
from procol.console import print_err

from .error import operational_error, integrity_error, programming_error, database_error, exception_on_statement, \
    DatabaseLocked


def _retry_on_locked_db(statement):

    def retry_statement(self, *args, **kwargs):
        while True:
            try:
                return statement(self, *args, **kwargs)
            except DatabaseLocked:
                print_err('Retrying: %s' % self)

    return retry_statement


class Sqlite3Statement(object):

    @_retry_on_locked_db
    def __call__(self, *args, **kwargs):
        try:
            return self._execute_statement(*args, **kwargs)
        except sqlite3.OperationalError, e:
            raise operational_error(self, e)
        except sqlite3.IntegrityError, e:
            raise integrity_error(self, e)
        except sqlite3.ProgrammingError, e:
            raise programming_error(self, e)
        except sqlite3.DatabaseError, e:
            raise database_error(self, e)
        except BaseException, e:
            raise exception_on_statement(self, e)

    def _execute_statement(self, *args, **kwargs):
        raise NotImplementedError