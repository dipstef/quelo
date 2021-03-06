import os

from ..error import DbError


class DbPathConnect(object):

    def __init__(self, _connection_class):
        self._connection_class = _connection_class

    def __call__(self, path, init_file=None):
        conn = self._connect(path, init_file=init_file)
        return conn

    def _connect(self, path, init_file=None):
        initialize = init_file and not os.path.exists(path)
        conn = self._connection_class(path)

        if initialize:
            self._load_db_structure(conn, path, init_file)
        return conn

    @staticmethod
    def _load_db_structure(conn, path, init_file):
        try:
            with open(init_file, mode='r') as script_init:
                statements = script_init.read()
                conn.execute_script(statements)
                conn.commit()
        except (DbError, OSError, IOError), e:
            conn.close()
            os.remove(path)
            raise e