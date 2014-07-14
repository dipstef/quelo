import os
from datetime import datetime

from urlo import Url
from dated import utc, datedtime
from quelo import get_value

import quelo
from quelo.sqlite import sqlite3


class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y


def adapt_point(point):
    return '%f;%f' % (point.x, point.y)

sqlite3.register_adapter(Point, adapt_point)


def test_custom_types():
    path = os.path.join(os.path.dirname(__file__), 'test.db')
    init_file = os.path.join(os.path.dirname(__file__), 'test.sql')

    with quelo.connect(path, init_file=init_file) as conn:

        with conn.cursor() as cursor:

            p = Point(4.0, -3.2)

            utc_now = datetime.utcnow()
            utc_converted = datedtime.from_datetime(utc_now)
            assert utc_now == utc_converted

            assert '4.000000;-3.200000' == get_value(cursor, 'select ?', (p,))
            assert utc_converted.to_string() == get_value(cursor, 'select ?', (utc_now,))
            assert utc_converted.to_string() == get_value(cursor, 'select ?', (utc_converted,))

            try:
                print cursor.select("select ?", (datedtime.now(),))
                assert False
            except:
                pass

            assert Url('http://test.com') == get_value(cursor, 'select ?', (Url('http://test.com'),))
            assert 'http://test.com' == get_value(cursor, 'select ?', (Url('http://test.com'),))

            cursor.execute('''insert into timestamp_value(value) values(?)  ''', (utc_now, ))

            assert utc_now == get_value(cursor, '''select value from timestamp_value
                                                    where value = ?  ''', (utc_now, ))

            assert utc_now == get_value(cursor, '''select value from timestamp_value
                                                    where value = ?  ''', (utc_converted, ))

            notz_utc = utc.now()
            cursor.execute('''insert into timestamp_value(value) values(?)  ''', (notz_utc, ))

            assert notz_utc == get_value(cursor, '''select value from timestamp_value
                                                    where value = ?  ''', (notz_utc, ))

            cursor.execute('''insert into url(value) values(?) ''', (Url('http://test.com'), ))

            assert Url('http://test.com') == get_value(cursor, '''select value from url
                                                                   where value = ?  ''', (Url('http://test.com'), ))

            assert 'http://test.com' == get_value(cursor, '''select value from url
                                                              where value = ?  ''', (Url('http://test.com'), ))

if __name__ == '__main__':
    test_custom_types()