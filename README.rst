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

    with quelo.connect('test.db', init_file='test.sql') as conn:
        with conn.cursor() as cursor:


Statements
==========

.. code-block:: python

    from quelo import get_value, get_column

        >>> cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('hulk', 'hogan'))
        >>> cursor.execute('''insert into full_name(name, surname) values(?,?) ''', ('mr', 't'))

        assert cursor.select('select name, surname from full_name') == [('hulk', 'hogan'), ('mr', 't')]
        assert get_column(cursor, '''select name from full_name''') == ['hulk', 'mr']

        assert get_value(cursor, 'select name from full_name where surname = ?', ('hogan', )) == 'hulk'

Errors
======

Unique Constraints

.. code-block:: python

    try:
        cursor.execute('''insert into full_name(name, surname)
                             values(?,?) ''', ('hulk', 'hogan'))

    except UniqueColumnsConstraintViolation, e:
         assert e.columns == ['name', 'surname']

    >>> e.message
        """UniqueColumnsConstraintViolation on ['name', 'surname'] in: Execute:
            insert into full_name(name, surname)
                                        values(?,?)  : ('hulk', 'hogan')"""

Primary key

.. code-block:: python

    full_name_id = get_value(cursor, '''select id
                                          from full_name
                                         where name = ?
                                           and surname = ? ''', ('hulk', 'hogan'))
    assert full_name_id is 1

    >>> cursor.execute('''insert into full_name(id, name, surname)
                             values(?,?,?) ''', (full_name_id, 'corky', 'butchek'))

    """PrimaryKeyViolation in: Execute:
        insert into full_name(id, name, surname)
                                    values(?,?,?)  : (1, 'corky', 'butchek') """

Foreign keys enabled by default

.. code-block:: python

    >>> cursor.execute('''insert into person(full_name_id, social_number)
                             values(?,?)''', (-1, 'the_hulk'))

    """ForeignKeyError in: Execute:
        insert into person(full_name_id, social_number)
                                    values(?,?) : (-1, 'the_hulk')"""