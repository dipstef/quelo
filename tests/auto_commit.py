import os

import quelo


def main():
    path = os.path.join(os.path.dirname(__file__), 'test.db')
    init_file = os.path.join(os.path.dirname(__file__), 'test.sql')

    #autocommit works for statement like create table, etc, but not on insert
    with quelo.connect(path, init_file) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''delete from test''')
            cursor.execute('''insert into test values(?)''', (1, ))

    conn.close()

    with quelo.connect(path, init_file) as conn:
        with conn.cursor() as cursor:
            assert not cursor.select('''select * from test ''')

if __name__ == '__main__':
    main()