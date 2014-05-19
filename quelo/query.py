def execute(c, statement, values_tuple):
    c.execute(statement, values_tuple)


def get_results(c, statement, query_tuple=None):
    return c.select(statement, query_tuple)


def get_row(c, statement, query_tuple=None):
    results = get_results(c, statement, query_tuple)
    return results[0] if results else None


def get_value(c, statement, query_tuple=None):
    result = get_row(c, statement, query_tuple)
    return result[0] if result else None


def get_value_rows(c, statement, query_tuple=None):
    results = get_results(c, statement, query_tuple)
    return [result[0] for result in results] if results else []