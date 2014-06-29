Quelo
=====

A friendly wrapper for Sqlite3

Features
========

Better error reporting, automatically retries a statement when the database file is locked.
General interface with multiple implementations, have a look at ``quecco`` and ``requem``.

Connecting
==========

Creates a database from a sql-statement file:

test.sql:


.. code-block:: sql

    create table full_name (
        id              integer not null primary key autoincrement,
        name            text not null,
        surname         text not null,
        unique(name, surname)
    );

    create table person (
        id                    integer not null primary key autoincrement,
        full_name_id          integer not null references full_name(id) on delete cascade,
        social_number         text not null,
        unique(social_number)
    );


.. code-block:: python

    import quelo
    from quelo import get_value, get_column

    with quelo.connect('test.db', init_file='test.sql') as conn:
        with conn.cursor() as cursor:


Statements
==========

.. code-block:: python


            >>> cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('hulk', 'hogan'))
            >>> cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('mr', 't'))

            assert cursor.select('select name, surname from full_name') == [('hulk', 'hogan'), ('mr', 't')]
            assert get_column(cursor, '''select name from full_name''') == ['hulk', 'mr']

            assert get_value(cursor, 'select name from full_name where surname = ?', ('hogan', )) == 'hulk'
