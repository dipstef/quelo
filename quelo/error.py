from unicoder import encoded


class DbError(Exception):
    def __init__(self, *args, **kwargs):
        super(DbError, self).__init__(*args, **kwargs)


class StatementException(DbError):
    def __init__(self, statement, *args):
        super(StatementException, self).__init__(*args)
        self._message = 'Exception on: %s %s' % (str(statement),  ' '.join((str(arg) for arg in args)))

    @property
    def message(self):
        return self._message

    def __str__(self):
        return encoded(self.message)


class StatementSyntaxError(StatementException):
    def __init__(self, statement, *args):
        super(StatementSyntaxError, self).__init__(statement, *args)


class TableNotExisting(StatementException):
    def __init__(self, statement, *args):
        super(TableNotExisting, self).__init__(statement, *args)


class StatementIntegrityError(StatementException):
    def __init__(self, statement, *args):
        super(StatementIntegrityError, self).__init__(statement, *args)


class ForeignKeyError(StatementIntegrityError):
    def __init__(self, statement, *args):
        super(ForeignKeyError, self).__init__(statement, *args)


class UniqueConstraintViolation(StatementIntegrityError):
    def __init__(self, statement, *args):
        super(UniqueConstraintViolation, self).__init__(statement, *args)


class PrimaryKeyViolation(UniqueConstraintViolation):
    def __init__(self, statement, *args):
        super(PrimaryKeyViolation, self).__init__(statement, *args)


class UniqueColumnsConstraintViolation(UniqueConstraintViolation):
    def __init__(self, statement, columns, *args):
        super(UniqueConstraintViolation, self).__init__(statement, *args)
        self.columns = columns


class StatementProgrammingError(StatementException):
    def __init__(self, statement, *args):
        super(StatementProgrammingError, self).__init__(statement, *args)


class ClosedCursor(StatementProgrammingError):
    def __init__(self, statement, *args):
        super(ClosedCursor, self).__init__(statement, *args)