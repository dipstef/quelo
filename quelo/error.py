from unicoder import encoded


class DbError(Exception):
    def __init__(self, *args, **kwargs):
        super(DbError, self).__init__(*args, **kwargs)


class StatementException(DbError):
    def __init__(self, statement, error, *args):
        super(StatementException, self).__init__(statement, error, *args)
        self.message = '%s in: %s' % (self.__class__.__name__, str(statement))
        self.cause = error

    def __str__(self):
        return encoded(self.message)


class StatementSyntaxError(StatementException):
    def __init__(self, statement, error, *args):
        super(StatementSyntaxError, self).__init__(statement, error, *args)


class TableNotExisting(StatementException):
    def __init__(self, statement, error):
        super(TableNotExisting, self).__init__(statement, error)


class StatementIntegrityError(StatementException):
    def __init__(self, statement, error, *args):
        super(StatementIntegrityError, self).__init__(statement, error, *args)


class ForeignKeyError(StatementIntegrityError):
    def __init__(self, statement, error):
        super(ForeignKeyError, self).__init__(statement, error)


class UniqueConstraintViolation(StatementIntegrityError):
    def __init__(self, statement, error, *args):
        super(UniqueConstraintViolation, self).__init__(statement, error, *args)


class PrimaryKeyViolation(UniqueConstraintViolation):
    def __init__(self, statement, error):
        super(PrimaryKeyViolation, self).__init__(statement, error)


class UniqueColumnsConstraintViolation(UniqueConstraintViolation):
    def __init__(self, statement, columns, error):
        super(UniqueConstraintViolation, self).__init__(statement, error, columns)
        self.columns = columns
        self.message = '%s on %s in: %s' % (self.__class__.__name__, columns, str(statement))


class StatementProgrammingError(StatementException):
    def __init__(self, statement, error):
        super(StatementProgrammingError, self).__init__(statement, error)


class ClosedCursor(StatementProgrammingError):
    def __init__(self, statement, *args):
        super(ClosedCursor, self).__init__(statement, *args)