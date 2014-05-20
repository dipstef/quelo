from contextlib import closing
import os

from ..error import DbError


class DbPathConnect(object):

    def __init__(self, _connection_class):
        self._connection_class = _connection_class

    def __call__(self, path, init_file=None):
        conn = self._connect(path, init_file=init_file)
        self._enable_foreign_keys(conn)
        return conn

    def _connect(self, path, init_file=None):
        conn = self._connection_class(path)
        if init_file and not os.path.exists(path):
            self._load_db_structure(conn, path, init_file)
        return conn

    @staticmethod
    def _load_db_structure(conn, path, init_file):
        try:
            with open(init_file, mode='r') as script_init:
                statements = script_init.read()
                conn.execute_script(statements)
                conn.commit()
        except DbError, e:
            conn.close()
            os.remove(path)
            raise e

    @staticmethod
    def _enable_foreign_keys(conn):
        with closing(conn.cursor()) as cursor:
            cursor.execute('''PRAGMA foreign_keys = ON''')
            conn.commit()
        return conn