from quelo.sqlite.error import _unique_columns_violation


def main():
    assert ['url'] == _unique_columns_violation('columns url is not unique')
    assert ['method', 'url'] == _unique_columns_violation('columns method, url are not unique')

if __name__ == '__main__':
    main()