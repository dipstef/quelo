def convert_custom_types(sqlite3):
    _register_no_tz_datetimes(sqlite3)


def _register_no_tz_datetimes(sqlite3):
    try:
        import dated
        from dated import notz

        def _to_datetime(value):
            assert not value.tzinfo
            return value.to_string()

        sqlite3.register_adapter(dated.datedtime, _to_datetime)
        sqlite3.register_adapter(dated.no_timezone, _to_datetime)
        sqlite3.register_adapter(notz.local, _to_datetime)
        sqlite3.register_adapter(notz.utc, _to_datetime)

    except ImportError, e:
        pass