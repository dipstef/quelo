import re

from ..error import DbError, StatementException, StatementSyntaxError, TableNotExisting, StatementIntegrityError, \
    ForeignKeyError, PrimaryKeyViolation, UniqueColumnsConstraintViolation, ClosedCursor


class DatabaseLocked(DbError):
    def __init__(self, statement, *args):
        super(DatabaseLocked, self).__init__('Database Locked while performing: %s ' % statement, *args)


class DatabaseCorrupted(StatementException):
    def __init__(self, statement, *args):
        super(DatabaseCorrupted, self).__init__(statement, *args)


class DatabaseIOError(StatementException):
    def __init__(self, statement, *args):
        super(DatabaseIOError, self).__init__(statement, *args)


def operational_error(statement, e):
    if e.message == 'database is locked':
        return DatabaseLocked(statement, e)
    elif 'syntax error' in e.message:
        return StatementSyntaxError(statement, e)
    elif 'no such table' in e.message:
        return TableNotExisting(statement, e)
    elif 'disk I/O error' in e.message:
        return DatabaseIOError(statement, e)
    else:
        return StatementException(statement, e)


_unique_violation = re.compile('column(s)?\s+(.+)\s+(is|are) not unique')
_primary_key_violation = re.compile('PRIMARY KEY must be unique')


def integrity_error(statement, e):
    if 'foreign key constraint failed' in e.message:
        return ForeignKeyError(statement, e)
    elif _primary_key_violation.search(e.message):
        raise PrimaryKeyViolation(statement, e)
    else:
        columns = _unique_columns_violation(e.message)
        if columns:
            return UniqueColumnsConstraintViolation(statement, columns, e)

    return StatementIntegrityError(statement, e)


def _unique_columns_violation(message):
    unique_violation = _unique_violation.search(message)
    if unique_violation:
        return [column.strip() for column in unique_violation.group(2).split(',')]


def programming_error(statement, e):
    if 'Cannot operate on a closed cursor' in e.message:
        return ClosedCursor(statement, e)
    else:
        return StatementIntegrityError(statement, e)


def database_error(statement, e):
    if 'database disk image is malformed' in e.message:
        return DatabaseCorrupted(statement, e)
    else:
        return DbError(e)


def exception_on_statement(statement, e):
    return StatementException(statement, e)